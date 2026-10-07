import contextlib
import hashlib
import hmac
import io
import json
import os
import sys
import tempfile
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'plugins/talentsia-work/server'))
import talentsia_agent as agent
import mcp_server
import setup_seat


class WorkSecurityTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.secret = 'ab' * 32
        self.profiles = self.root / 'agents.json'
        self.profiles.write_text(json.dumps({
            name: {'id': name, 'key': self.secret, 'workspace': 'https://example.test/agents/v1'}
            for name in ('designer', 'engineer')
        }))
        self.profiles.chmod(0o600)
        # mcp_server loads its own copy of the client, so both copies are
        # pointed at the synthetic file. Patching only one let a test reach
        # the developer's real ~/.talentsia/agents.json and a real workspace.
        for module in (agent, mcp_server.agent):
            redirect = patch.object(module, 'PROFILES', self.profiles)
            redirect.start()
            self.addCleanup(redirect.stop)
        environment = patch.dict(os.environ, {name: '' for name in (
            'TALENTSIA_AGENT_ID', 'TALENTSIA_AGENT_KEY', 'TALENTSIA_WORKSPACE')})
        environment.start()
        self.addCleanup(environment.stop)
        # No test reaches the network: one that forgets to fake it fails here.
        offline = patch('urllib.request.OpenerDirector.open',
                        side_effect=AssertionError('a test tried to reach the network'))
        self.network = offline.start()
        self.addCleanup(offline.stop)

    def test_keys_exact_length_and_never_echoed(self):
        for value in (self.secret + 'Z', self.secret * 2, 'SYNTHETIC_SECRET', self.secret[:62]):
            with self.subTest(length=len(value)), self.assertRaises(SystemExit) as refusal:
                agent._key(value, 'test')
            self.assertNotIn(value, str(refusal.exception))
        self.assertEqual(agent._key(self.secret, 'test'), bytes.fromhex(self.secret))

    @unittest.skipUnless(os.name == 'posix', 'POSIX permissions')
    def test_runtime_rejects_world_readable_credentials(self):
        self.profiles.chmod(0o644)
        with self.assertRaises(SystemExit):
            agent._credentials('designer')

    def test_invalid_profile_shape_is_redacted(self):
        for value in ('[]', json.dumps({'designer': self.secret})):
            self.profiles.write_text(value)
            with self.assertRaises(SystemExit) as refusal:
                agent._profiles()
            self.assertNotIn(self.secret, str(refusal.exception))

    def test_no_default_for_multiple_seats(self):
        with self.assertRaises(SystemExit):
            agent._credentials()
        self.assertEqual(agent._credentials('designer')[0], 'designer')
        self.assertEqual(agent._credentials('engineer')[0], 'engineer')

    def test_single_profile_selected(self):
        profile = agent._profiles()['designer']
        self.profiles.write_text(json.dumps({'designer': profile}))
        self.assertEqual(agent._credentials()[0], 'designer')

    def test_environment_fallback(self):
        self.profiles.unlink()
        with patch.dict(os.environ, {'TALENTSIA_AGENT_ID': 'test', 'TALENTSIA_AGENT_KEY': self.secret,
                                     'TALENTSIA_WORKSPACE': 'https://example.test/agents/v1'}):
            self.assertEqual(agent._credentials()[0], 'test')

    def test_unsafe_workspaces_rejected(self):
        for base in ('http://example.test/agents/v1', 'https://user:pass@example.test/agents/v1',
                     'https://example.test/agents/v1?token=secret', 'https://example.test/agents/v1#secret',
                     'https://example.test/other', 'https://example.test:invalid/agents/v1'):
            with self.subTest(base=base), self.assertRaises(SystemExit):
                agent._workspace(base)

    def test_path_cannot_change_signed_request(self):
        for path in ('tasks?state=secret', '../tasks', 'tasks#secret', 'tasks/1/../2', '//other.test/tasks'):
            with self.subTest(path=path), self.assertRaises(SystemExit):
                agent.call(path, acting='designer')

    def test_redirects_are_not_followed(self):
        request = urllib.request.Request('https://example.test/agents/v1/tasks')
        for code in (301, 302, 303, 307, 308):
            with self.subTest(code=code), self.assertRaises(urllib.error.HTTPError):
                agent._NoRedirect().redirect_request(request, None, code, '', {}, 'https://other.test/')

    def test_error_bodies_do_not_enter_mcp_output(self):
        for code in (401, 403, 500):
            error = urllib.error.HTTPError('https://example.test', code, self.secret, {}, io.BytesIO(self.secret.encode()))
            with patch('urllib.request.OpenerDirector.open', side_effect=error):
                answer = mcp_server._invoke('my_tasks', {}, 'designer')
            self.assertTrue(answer['isError'])
            self.assertNotIn(self.secret, json.dumps(answer))

    def test_every_tool_sends_its_request(self):
        """Each tool's request passes the client's own path check and reaches the network.

        my_tasks once built `tasks?state=...`, which the client refuses, so
        the seat's first call failed for every user while every other test
        passed: a refusal before the network looks exactly like an error from it.
        """
        sample = {'taskId': '7', 'artifactId': '3', 'commitmentId': '2', 'note': 'n', 'state': 'on_track',
                  'title': 't', 'body': 'b', 'goal': 'g', 'what': 'w', 'because': 'because so'}
        for tool in mcp_server.TOOLS:
            if tool['call'] == 'media':
                continue
            with self.subTest(tool=tool['name']), patch(
                    'urllib.request.OpenerDirector.open', return_value=io.BytesIO(b'{"items": []}')) as opened:
                answer = mcp_server._invoke(tool['name'], dict(sample), 'designer')
                self.assertFalse(answer.get('isError'), answer)
                self.assertTrue(opened.called)
                self.assertNotIn('?', opened.call_args.args[0].full_url)

    def test_my_tasks_filters_locally_and_says_what_it_searched(self):
        items = [{'id': str(n), 'taskState': 'ready' if n % 3 == 0 else 'completed'} for n in range(40)]
        with patch('urllib.request.OpenerDirector.open',
                   return_value=io.BytesIO(json.dumps({'items': items}).encode())):
            answer = mcp_server._invoke('my_tasks', {'state': 'ready', 'limit': 5}, 'designer')
        shown = json.loads(answer['content'][0]['text'])
        self.assertEqual([i['taskState'] for i in shown['items']], ['ready'] * 5)
        self.assertIn('14 of the 40 most recent', shown['note'])
        self.assertIn('an older task can still exist', shown['note'])

    def test_signature_covers_body_method_path_and_seat(self):
        response = io.BytesIO(b'{}')
        with patch('urllib.request.OpenerDirector.open', return_value=response) as opened:
            agent.call('tasks/1/progress', {'note': 'synthetic'}, acting='designer')
        request = opened.call_args.args[0]
        headers = {name.lower(): value for name, value in request.header_items()}
        material = '\n'.join(('POST', '/agents/v1/tasks/1/progress', headers['x-talentsia-timestamp'],
                              headers['x-talentsia-nonce'], hashlib.sha256(request.data).hexdigest()))
        expected = hmac.new(bytes.fromhex(self.secret), material.encode(), hashlib.sha256).hexdigest()
        self.assertEqual(headers['x-talentsia-signature'], expected)
        self.assertEqual(headers['x-talentsia-agent'], 'designer')
        self.assertNotIn(self.secret, json.dumps(headers))

    def test_picture_limit_and_type(self):
        image = self.root / 'picture.png'
        image.write_bytes(b'\x89PNG\r\n\x1a\n')
        self.assertEqual(mcp_server._picture({'path': str(image)})[1]['type'], 'image/png')
        image.write_bytes(b'RIFF0000WAVE')
        with self.assertRaises(SystemExit):
            mcp_server._picture({'path': str(image)})
        with image.open('wb') as output:
            output.truncate(8 * 1024 * 1024 + 1)
        with self.assertRaises(SystemExit):
            mcp_server._picture({'path': str(image)})
        with self.assertRaises(SystemExit):
            mcp_server._picture({'path': str(self.profiles)})

    def test_unexpected_exception_details_are_hidden(self):
        with patch.object(mcp_server.agent, 'call', side_effect=ValueError(self.secret)):
            result = mcp_server._invoke('my_tasks', {}, 'designer')
        self.assertTrue(result['isError'])
        self.assertNotIn(self.secret, json.dumps(result))

    def test_setup_pins_file_and_never_writes_key(self):
        for harness, suffix in (('codex', 'toml'), ('claude', 'md')):
            target = self.root / f'{harness}.{suffix}'
            with patch.object(setup_seat, '_target', return_value=target), \
                 patch.object(setup_seat, 'install', return_value=self.root / 'bin'), \
                 contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(setup_seat.write_agent(harness, 'designer', 'content-designer', '', str(self.profiles), False), 0)
            self.assertIn(str(self.profiles), target.read_text())
            self.assertNotIn(self.secret, target.read_text() + output.getvalue())

    def test_setup_refuses_invalid_credentials_before_install(self):
        self.profiles.write_text('[]')
        with patch.object(setup_seat, 'install') as installed, contextlib.redirect_stdout(io.StringIO()):
            result = setup_seat.write_agent('codex', 'designer', 'content-designer', '', str(self.profiles), False)
        self.assertEqual(result, 1)
        installed.assert_not_called()


if __name__ == '__main__':
    unittest.main()