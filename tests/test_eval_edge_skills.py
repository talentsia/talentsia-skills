"""The skill eval harness, proved against a fake Ollama on loopback.

Nothing here reaches a real model. A local HTTP server speaks just enough of
/api/chat to play back scripted tool calls and to judge statements by
substring, so what is under test is the harness: what it renders, what it
offers, what it feeds back, how it grades, and what it writes.
"""
import contextlib
import io
import json
import shutil
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import eval_edge_skills as harness  # noqa: E402


def call(name, **arguments):
    return {"role": "assistant", "content": "", "tool_calls": [{"function": {"name": name, "arguments": arguments}}]}


def calls(*names):
    return {"role": "assistant", "content": "",
            "tool_calls": [{"function": {"name": n, "arguments": {}}} for n in names]}


def say(text):
    return {"role": "assistant", "content": text}


class FakeOllama:
    """/api/chat on 127.0.0.1. Agent turns follow a script keyed by the goal;
    judge turns (no tools) answer YES when the statement is in the answer."""

    def __init__(self):
        self.scripts = {}
        self.requests = []
        self.fail_with = None
        fake = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                fake.requests.append(body)
                if fake.fail_with or self.path != "/api/chat":
                    self.send_response(fake.fail_with or 404)
                    self.end_headers()
                    self.wfile.write(b"boom")
                    return
                payload = json.dumps({"model": body["model"], "message": fake.respond(body), "done": True}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}"
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def respond(self, body):
        if not body.get("tools"):
            prompt = body["messages"][-1]["content"]
            if "Statement: " in prompt:
                answer = prompt.split("<<<\n", 1)[1].split("\n>>>", 1)[0]
                statement = prompt.split("Statement: ", 1)[1].split("\n", 1)[0]
                return say("YES" if statement.lower() in answer.lower() else "NO.")
        goal = body["messages"][1]["content"]
        script = self.scripts[goal]
        return script.pop(0) if len(script) > 1 else script[0]

    def agent_requests(self):
        return [r for r in self.requests if r.get("tools")]

    def close(self):
        self.server.shutdown()
        self.server.server_close()


class HarnessTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        # A copy, so --write-results can be checked without touching the repo.
        self.root = Path(temporary.name)
        shutil.copytree(ROOT / "capabilities", self.root / "capabilities")
        shutil.copytree(ROOT / "plugins" / "talentsia-bookkeeping", self.root / "plugins" / "talentsia-bookkeeping")
        self.ollama = FakeOllama()
        self.addCleanup(self.ollama.close)
        harness.use_root(self.root)
        self.addCleanup(harness.use_root, ROOT)

    def skill(self, name):
        package = json.loads((self.root / "plugins/talentsia-bookkeeping/talentsia-package.json").read_text())
        return harness.load_skill(package["name"], self.root / "plugins/talentsia-bookkeeping/skills" / name)

    def run_harness(self, *argv):
        out = self.root / "out.json"
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(io.StringIO()):
            status = harness.main(["--root", str(self.root), "--base-url", self.ollama.url,
                                   "--model", "scripted", "--package", "bookkeeping",
                                   "--json", str(out), *argv])
        report = json.loads(out.read_text()) if out.exists() else None
        return status, report, stdout.getvalue()

    def case_result(self, report, case_id):
        return next(c for s in report["skills"] for c in s["cases"] if c["id"] == case_id)

    # --- rendering and tools ---

    def test_compact_form_for_a_small_model_and_full_form_otherwise(self):
        skill = self.skill("work-a-statement")
        compact = harness.system_prompt(skill, "small-local")
        full = harness.system_prompt(skill, "large-local")
        self.assertIn("Never state a fact you have not observed with a tool", compact)
        for section in ("When to use:", "Steps:", "Done when:"):
            self.assertIn(section, compact)
        self.assertNotIn("Notes:", compact)
        self.assertIn("Notes:", full)
        self.assertIn("45 of 53 rows", full)
        self.assertIn("ledger_statements_import_import stages every row", compact)
        self.assertIn("agent_place-rows", compact)
        self.assertNotIn("{{", full)

    def test_every_operation_of_every_required_interface_is_offered(self):
        tools, names = harness.offered_tools(self.skill("work-a-statement"))
        self.assertEqual(set(names), {
            "ledger_statements_import_import", "ledger_statements_import_review_queue",
            "ledger_statements_import_categorise", "ledger_chart_read_accounts",
            "ledger_reconcile_reconcile", "operator_notify_notify", "agent_place-rows"})
        self.assertEqual(names["agent_place-rows"], "agent:place-rows")
        by_name = {t["function"]["name"]: t["function"] for t in tools}
        self.assertEqual(by_name["ledger_reconcile_reconcile"]["description"],
                         "Prove the books against a statement's closing balance. Operation: reconcile.")
        self.assertEqual(by_name["agent_place-rows"]["description"],
                         "Assign each staged statement row to an account in the entity's chart.")
        self.assertTrue(by_name["operator_notify_notify"]["parameters"]["additionalProperties"])
        self.assertEqual(by_name["operator_notify_notify"]["parameters"]["required"], [])

    def test_verdicts_are_parsed_strictly(self):
        self.assertTrue(harness.parse_verdict("YES"))
        self.assertTrue(harness.parse_verdict(" **Yes.** it does"))
        self.assertFalse(harness.parse_verdict("NO"))
        self.assertIsNone(harness.parse_verdict("Probably"))
        self.assertIsNone(harness.parse_verdict(""))

    # --- the loop and grading ---

    def test_calls_and_not_calls_are_graded_from_what_was_called(self):
        self.ollama.scripts["Work the statement."] = [
            calls("ledger_statements_import_import", "ledger_reconcile_reconcile"),
            say("Imported and reconciled.")]
        status, report, out = self.run_harness("--skill", "work-a-statement", "--case", "reconciles-or-says-why")
        self.assertEqual(status, 1)
        result = self.case_result(report, "reconciles-or-says-why")
        self.assertFalse(result["passed"])
        self.assertEqual(result["failures"], ["calls: operator.notify/notify was never called",
                                              "notCalls: ledger.reconcile/reconcile was called"])
        self.assertIn("FAIL  reconciles-or-says-why", out)
        self.assertIn("- notCalls: ledger.reconcile/reconcile was called", out)
        # The recorded observation is what the worker was shown for that call,
        # and an operation the case recorded nothing for gets the neutral one.
        tool_turns = [m for m in self.ollama.agent_requests()[1]["messages"] if m["role"] == "tool"]
        self.assertEqual(tool_turns[0], {"role": "tool", "tool_name": "ledger_statements_import_import",
                                         "content": "12 rows; the statement prints no closing balance"})
        self.assertEqual(tool_turns[1]["content"], harness.NEUTRAL_OBSERVATION)

    def test_a_case_passes_when_every_expectation_holds(self):
        self.ollama.scripts["Work the statement."] = [
            calls("ledger_statements_import_import"), call("operator_notify_notify", message="no closing balance"),
            say("Imported 12 rows; told a person there is no closing balance.")]
        status, report, out = self.run_harness("--skill", "work-a-statement", "--case", "reconciles-or-says-why")
        self.assertEqual(status, 0, out)
        result = self.case_result(report, "reconciles-or-says-why")
        self.assertTrue(result["passed"])
        self.assertEqual([c["reference"] for c in result["calls"]],
                         ["ledger.statements.import/import", "operator.notify/notify"])
        self.assertEqual(result["calls"][1]["arguments"], {"message": "no closing balance"})
        self.assertEqual(report["skills"][0]["passRate"], 1.0)

    def test_subagents_are_graded_and_answered(self):
        self.ollama.scripts["Work the September statement."] = [
            calls("ledger_statements_import_import"), say("Imported.")]
        status, report, _ = self.run_harness("--skill", "work-a-statement", "--case", "imported-whole")
        self.assertEqual(status, 1)
        self.assertEqual(self.case_result(report, "imported-whole")["failures"],
                         ["agents: place-rows was never started"])

        self.ollama.scripts["Work the September statement."] = [
            calls("ledger_statements_import_import", "agent_place-rows"), say("Imported and placed.")]
        status, report, _ = self.run_harness("--skill", "work-a-statement", "--case", "imported-whole")
        self.assertEqual(status, 0)
        tool_turns = [m for m in self.ollama.agent_requests()[-1]["messages"] if m["role"] == "tool"]
        self.assertEqual(tool_turns[-1]["content"], harness.AGENT_OBSERVATION)

    def test_says_and_not_says_are_put_to_the_judge(self):
        goal = next(c for c in self.skill("choose-the-account").cases
                    if c["id"] == "purpose-not-payee")["given"]["goal"]
        self.ollama.scripts[goal] = [calls("ledger_chart_read_accounts"), say("Placed on 6100 Repairs.")]
        status, report, _ = self.run_harness("--skill", "choose-the-account", "--case", "purpose-not-payee")
        self.assertEqual(status, 0)
        judged = [r for r in self.ollama.requests if not r.get("tools")]
        self.assertEqual(len(judged), 1)
        self.assertEqual(judged[0]["options"], {"temperature": 0.0, "seed": 1, "num_ctx": 16384})
        self.assertIn("Statement: 6100", judged[0]["messages"][-1]["content"])

        self.ollama.scripts[goal] = [calls("ledger_chart_read_accounts"), say("Placed on Repairs.")]
        status, report, _ = self.run_harness("--skill", "choose-the-account", "--case", "purpose-not-payee")
        self.assertEqual(status, 1)
        self.assertEqual(self.case_result(report, "purpose-not-payee")["failures"],
                         ["says: the answer does not say '6100'"])

    def test_not_says_fails_when_the_answer_says_it(self):
        goal = next(c for c in self.skill("choose-the-account").cases if c["id"] == "only-listed-accounts")["given"]["goal"]
        self.ollama.scripts[goal] = [calls("ledger_chart_read_accounts"), say("I put it on Software expense.")]
        status, report, _ = self.run_harness("--skill", "choose-the-account", "--case", "only-listed-accounts")
        self.assertEqual(status, 1)
        self.assertEqual(self.case_result(report, "only-listed-accounts")["failures"],
                         ["notSays: the answer says 'Software expense'"])

    def test_context_observations_open_the_job(self):
        self.ollama.scripts["Record the plumber's bill."] = [say("Nothing to do.")]
        self.run_harness("--skill", "record-what-is-owed", "--case", "no-due-date-flagged")
        messages = self.ollama.agent_requests()[0]["messages"]
        self.assertEqual(messages[2]["tool_calls"], [{"function": {"name": "document", "arguments": {}}}])
        self.assertEqual(messages[3], {"role": "tool", "tool_name": "document", "content": "Plumber: 320.00, no due date"})

    def test_a_tool_never_offered_is_recorded_and_refused(self):
        self.ollama.scripts["Record the plumber's bill."] = [calls("sudo_bash"), say("Done.")]
        _, report, _ = self.run_harness("--skill", "record-what-is-owed", "--case", "no-due-date-flagged")
        result = self.case_result(report, "no-due-date-flagged")
        self.assertEqual(result["calls"][0]["reference"], None)
        tool_turn = [m for m in self.ollama.agent_requests()[1]["messages"] if m["role"] == "tool"][-1]
        self.assertIn("no tool named sudo_bash", tool_turn["content"])

    def test_the_loop_is_bounded_and_still_asks_for_an_answer(self):
        self.ollama.scripts["Record the plumber's bill."] = [calls("ledger_review_flag_flag")]
        _, report, _ = self.run_harness("--skill", "record-what-is-owed", "--case", "no-due-date-flagged")
        result = self.case_result(report, "no-due-date-flagged")
        self.assertEqual(result["turns"], harness.MAX_TURNS)
        self.assertEqual(len(result["calls"]), harness.MAX_TURNS)
        agent_turns = [r for r in self.ollama.requests if r["messages"][1]["content"] == "Record the plumber's bill."]
        self.assertEqual(len(agent_turns), harness.MAX_TURNS + 1)
        self.assertNotIn("tools", agent_turns[-1])
        self.assertTrue(result["passed"])

    # --- publishing ---

    def test_write_results_records_the_pass_rate_in_the_files_own_format(self):
        cases = self.skill("record-what-is-owed").cases
        goals = {c["id"]: c["given"]["goal"] for c in cases}
        self.ollama.scripts[goals["bill-not-payment"]] = [
            calls("ledger_bills_write_record_bill", "ledger_reports_read_open_payables"), say("ACME 1,240.00 is open.")]
        self.ollama.scripts[goals["no-due-date-flagged"]] = [calls("ledger_review_flag_flag"), say("Flagged.")]
        self.ollama.scripts[goals["read-back"]] = [say("Recorded 89.12.")]  # never reads it back
        spec_path = self.root / "plugins/talentsia-bookkeeping/skills/record-what-is-owed/skill.json"
        before = json.loads(spec_path.read_text())

        status, report, out = self.run_harness("--skill", "record-what-is-owed", "--write-results")

        self.assertEqual(status, 1)
        self.assertIn("pass rate 2/3 = 0.67", out)
        self.assertEqual(report["skills"][0]["passRate"], 0.67)
        before["model"]["evals"]["scripted"] = 0.67
        self.assertEqual(spec_path.read_text(), json.dumps(before, indent=2) + "\n")

    def test_a_server_error_is_not_a_failed_case_and_writes_nothing(self):
        self.ollama.fail_with = 500
        spec_path = self.root / "plugins/talentsia-bookkeeping/skills/record-what-is-owed/skill.json"
        before = spec_path.read_text()
        status, report, out = self.run_harness("--skill", "record-what-is-owed", "--write-results")
        self.assertEqual(status, 2)
        self.assertIn("ERROR", out)
        self.assertTrue(report["skills"][0]["errored"])
        self.assertEqual(spec_path.read_text(), before)

    def test_a_skill_the_validator_refuses_is_not_evaluated(self):
        skill_md = self.root / "plugins/talentsia-bookkeeping/skills/record-what-is-owed/SKILL.md"
        skill_md.write_text(skill_md.read_text().replace("## Done when", "## Finished when"))
        status, report, out = self.run_harness("--skill", "record-what-is-owed")
        self.assertEqual(status, 2)
        self.assertIsNone(report)
        self.assertIn("INVALID", out)
        self.assertEqual(self.ollama.requests, [])

    def test_fake_mode_never_writes_results(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            harness.main(["--fake", "--write-results"])


class FakeModeOverTheRepository(unittest.TestCase):
    def test_every_case_in_the_repository_is_reachable(self):
        """The oracle calls exactly what each case expects. A failure here is a
        case expecting something the rendered skill does not offer."""
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            status = harness.main(["--fake"])
        self.assertEqual(status, 0, out.getvalue())


if __name__ == "__main__":
    unittest.main()
