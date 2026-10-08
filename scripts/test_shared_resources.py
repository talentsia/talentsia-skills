"""Generic public regression cases; no product content or customer evidence."""
# Copyright (c) 2026 Talentsia. SPDX-License-Identifier: MIT
import hashlib
import io
import json
import stat
import tempfile
import unittest
import zipfile
from pathlib import Path

from shared_resources import ResourceError, archive, safe_path, validate_resources, verify_archive


def fixture():
    fields = {'name': 'analyst', 'description': 'Review supplied evidence.', 'tools': [],
              'model': 'small-local', 'maxSteps': 1, 'input': {'evidence': 'Supplied excerpts'},
              'output': {'type': 'object', 'required': ['result'], 'additionalProperties': False,
                         'properties': {'result': {'type': 'string'}}}}
    role = '---\n' + '\n'.join(f'{k}: {json.dumps(v)}' for k,v in fields.items())
    role += '\n---\n\n## Steps\n\n1. Review evidence.\n\n## Done when\n\n- Return the cited result.\n'
    return {'SKILL.md': b'# Example\nAssign {{agent:analyst}}. Read [method](references/core.md#checks).\n',
            'agents/analyst.md': role.encode(), 'references/core.md': b'# Method\n## Checks\n'}, {'subagents': ['analyst']}


class ResourceTests(unittest.TestCase):
    def assert_invalid(self, files, metadata):
        with self.assertRaises(ResourceError):
            validate_resources(files, metadata)

    def test_complete_skill(self):
        validate_resources(*fixture())

    def test_missing_declared_role(self):
        files, metadata = fixture()
        del files['agents/analyst.md']
        self.assert_invalid(files, metadata)

    def test_missing_reference_and_anchor(self):
        files, metadata = fixture()
        files['references/core.md'] = b'# Method\n'
        self.assert_invalid(files, metadata)
        del files['references/core.md']
        self.assert_invalid(files, metadata)

    def test_undeclared_or_unused_role(self):
        files, metadata = fixture()
        metadata['subagents'] = []
        self.assert_invalid(files, metadata)
        files, metadata = fixture()
        files['SKILL.md'] = b'# Example\n'
        self.assert_invalid(files, metadata)
        files, metadata = fixture()
        files['agents/unused.md'] = b'# Undeclared role\n'
        self.assert_invalid(files, metadata)

    def test_role_schema_and_step_contract(self):
        for old,new in [(b'"required": ["result"]',b'"required": "result"'),
                        (b'maxSteps: 1',b'maxSteps: 7'),
                        (b'1. Review evidence.',b'2. Review evidence.')]:
            files, metadata = fixture()
            files['agents/analyst.md'] = files['agents/analyst.md'].replace(old,new)
            self.assert_invalid(files,metadata)

    def test_schema_references(self):
        files, metadata = fixture()
        files['references/result.schema.json'] = b'{"$ref":"defs.json#/$defs/result"}'
        self.assert_invalid(files, metadata)
        files['references/defs.json'] = b'{"$defs":{"result":{"type":"string"}}}'
        validate_resources(files, metadata)
        files['references/result.schema.json'] = b'{"$ref":"defs.json#/$defs/absent"}'
        self.assert_invalid(files, metadata)

    def test_nested_schema_structure(self):
        files, metadata = fixture()
        files['references/result.schema.json'] = b'{"type":"object","properties":{"result":{"allOf":[{"type":"invalid"}]}}}'
        self.assert_invalid(files,metadata)

    def test_embedded_role_schema_local_reference(self):
        files, metadata = fixture()
        files['agents/analyst.md'] = files['agents/analyst.md'].replace(
            b'"properties": {"result": {"type": "string"}}',
            b'"properties": {"result": {"$ref": "#/$defs/value"}}, "$defs": {"value": {"type": "string"}}')
        validate_resources(files, metadata)
        files['agents/analyst.md'] = files['agents/analyst.md'].replace(b'#/$defs/value',b'#/$defs/missing')
        self.assert_invalid(files,metadata)

    def test_malformed_required_arrays(self):
        for required in ('"result"','[1]','["result","result"]'):
            files, metadata = fixture()
            files['references/result.schema.json'] = ('{"type":"object","required":'+required+'}').encode()
            self.assert_invalid(files,metadata)

    def test_unsafe_paths(self):
        for path in ('../a','/a','C:/a','a\\b','.git/config','.env','.env.production','.ENV.test','secrets/token.json','a\nname','run-record.json','runtime-records/session.json','work/session.md','x/private-scenarios/client.json','approvals/release.json','a//b','a/./b'):
            with self.subTest(path=path),self.assertRaises(ResourceError):
                safe_path(path)

    def test_deterministic_archive_and_round_trip(self):
        files,_ = fixture()
        blob = archive(files)
        self.assertEqual(blob,archive(dict(reversed(list(files.items())))))
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'skill.zip'
            path.write_bytes(blob)
            self.assertEqual(files,verify_archive(path,hashlib.sha256(blob).hexdigest()))
            with self.assertRaises(ResourceError):
                verify_archive(path,'0'*64)

    def test_malicious_archives(self):
        for name,mode,duplicate in [('../escape',stat.S_IFREG,False),('role.md',stat.S_IFLNK,False),('role.md',stat.S_IFREG,True)]:
            with self.subTest(name=name,mode=mode,duplicate=duplicate),tempfile.TemporaryDirectory() as folder:
                path=Path(folder)/'unsafe.zip'
                with zipfile.ZipFile(path,'w') as z:
                    entry=zipfile.ZipInfo(name)
                    entry.external_attr=(mode|0o644)<<16
                    z.writestr(entry,b'payload')
                    if duplicate:
                        z.writestr(entry,b'second')
                with self.assertRaises(ResourceError):
                    verify_archive(path,hashlib.sha256(path.read_bytes()).hexdigest())


if __name__ == '__main__':
    unittest.main()
