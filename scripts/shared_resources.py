"""Generic self-contained skill resource checks and deterministic safe archives.

These checks establish structural integrity, never runtime behavior or release approval.
No service credentials or content-specific knowledge belongs in this module.
"""
# Copyright (c) 2026 Talentsia. SPDX-License-Identifier: MIT
# Generic improvement derived from Talentsia Skill Builder 0.1.0 resource,
# subagent, and export contracts. No premium workflows or evidence are included.
from __future__ import annotations

import hashlib
import io
import json
import posixpath
import re
import stat
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit


class ResourceError(ValueError):
    pass


FORBIDDEN = {'.git', '.github', '.env', '.env.local', '.ds_store', '__pycache__',
             'node_modules', 'work', 'work-records', 'scenarios-reference',
             'private-scenarios', 'approvals', 'credentials', 'caches', 'cache',
             '.cache', '.venv', '.ssh', '.talentsia', 'secrets', '.credentials',
             'runtime-records', 'run-records', 'private-records'}
MAX_FILES = 10000
MAX_BYTES = 100 * 1024 * 1024

# Reviewed Talentsia Skill Builder 0.1.0 capability vocabulary, also present in
# public capabilities/v1.json. A newer trusted pinned vocabulary can be supplied;
# declarations themselves never create interfaces or grant tool access.
BUILDER_CAPABILITIES = {
    'documents.inspect': ('inspect', 'extract_text', 'metadata'),
    'documents.register': ('register',), 'files.workspace': ('list', 'read', 'write', 'move', 'mkdir'),
    'host.observe': ('system', 'services', 'logs'), 'host.services.restart': ('restart',),
    'operator.notify': ('notify',), 'memory.learn': ('learn', 'recall'),
    'work.history.read': ('activity', 'outcomes'), 'team.read': ('roster', 'context', 'gaps'),
    'artifacts.read': ('list', 'search', 'read'), 'artifacts.dispose': ('dispose',),
    'work.handoff': ('delegate',), 'decisions.prepare': ('raise',), 'staffing.request': ('request',),
    'commitments.mine': ('list', 'update'), 'intent.read': ('priorities', 'measures'),
    'intent.propose': ('propose',), 'commitments.read': ('list',),
    'commitments.write': ('record', 'update', 'date'), 'decisions.read': ('list',),
    'briefs.write': ('brief', 'meeting_brief'), 'attention.read': ('inbox', 'attention'),
    'attention.write': ('record',), 'calendar.read': ('today', 'week', 'meeting', 'categorise'),
    'drafts.write': ('draft_reply',), 'ledger.entity.read': ('entity', 'partners'),
    'ledger.chart.read': ('accounts',),
    'ledger.reports.read': ('open_payables', 'entries', 'entry', 'expense_summary', 'financial_summary'),
    'ledger.documents.lookup': ('find_by_document',), 'ledger.bills.write': ('record_bill', 'add_contact'),
    'ledger.payments.write': ('record_payment', 'record_receipt'),
    'ledger.statements.import': ('import', 'review_queue', 'categorise'), 'ledger.reconcile': ('reconcile',),
    'ledger.review.flag': ('flag',), 'code.repo.read': ('repos', 'files', 'read', 'search'),
    'code.repo.write': ('write', 'replace'), 'code.checks.run': ('check',),
    'code.change.prepare': ('diff', 'prepare'), 'code.preview': ('preview',),
    'tasks.write': ('create', 'update'),
}


def _capabilities(metadata, vocabulary):
    values = metadata.get('requires', {}).get('capabilities')
    if not isinstance(values, list) or any(not isinstance(v, str) for v in values) or len(set(values)) != len(values):
        raise ResourceError('invalid required capability inventory')
    interfaces = set()
    for value in values:
        interface, separator, version = value.partition('@')
        if not separator or version != '1' or interface not in vocabulary:
            raise ResourceError(f'unresolved required capability: {value}')
        interfaces.add(interface)
    return interfaces


def _operation(value, interfaces, vocabulary):
    if not isinstance(value, str) or value.count('/') != 1:
        raise ResourceError(f'invalid tool operation: {value!r}')
    interface, operation = value.split('/')
    if interface not in interfaces or operation not in vocabulary.get(interface, ()):
        raise ResourceError(f'unresolved or undeclared tool operation: {value}')


def validate_builder_cases(value: dict, identifier: str, metadata: dict | None = None,
                           capabilities: dict | None = None) -> None:
    """Check authored graded case contracts, without executing or grading them.

    Pass canonical builder metadata to enforce exact role/capability membership.
    Standalone callers still receive schema, vocabulary and scenario checks.
    """
    vocabulary = BUILDER_CAPABILITIES if capabilities is None else capabilities
    if not isinstance(value, dict) or value.get('schema') != 'talentsia-skill-evals/v1' or value.get('skill') != identifier:
        raise ResourceError('evaluation schema or skill identity mismatch')
    cases = value.get('cases')
    if not isinstance(cases, list) or not 3 <= len(cases) <= 6:
        raise ResourceError('builder evaluations require three to six cases')
    interfaces = _capabilities(metadata, vocabulary) if metadata is not None else set(vocabulary)
    agents = set(metadata.get('subagents', [])) if metadata is not None else None
    seen, regression = set(), False
    for case in cases:
        if not isinstance(case, dict):
            raise ResourceError('evaluation case must be an object')
        identifier_case = case.get('id')
        if not isinstance(identifier_case, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', identifier_case) or identifier_case in seen:
            raise ResourceError('evaluation case IDs must be unique kebab names')
        seen.add(identifier_case)
        if not isinstance(case.get('title'), str) or not case['title'].strip():
            raise ResourceError(f'{identifier_case}: missing case title')
        if 'regression' in case and type(case['regression']) is not bool:
            raise ResourceError(f'{identifier_case}: regression flag must be boolean')
        regression |= case.get('regression') is True
        given, expect = case.get('given'), case.get('expect')
        if not isinstance(given, dict) or not isinstance(given.get('goal'), str) or not given['goal'].strip() or not isinstance(given.get('observations'), dict):
            raise ResourceError(f'{identifier_case}: goal and observations are required')
        if not isinstance(expect, dict) or not expect or set(expect) - {'calls', 'notCalls', 'agents', 'says', 'notSays'}:
            raise ResourceError(f'{identifier_case}: invalid grading contract')
        has_expectation = False
        for key, expectations in expect.items():
            if not isinstance(expectations, list) or any(not isinstance(x, str) or not x.strip() for x in expectations) or len(set(expectations)) != len(expectations):
                raise ResourceError(f'{identifier_case}: invalid {key} expectations')
            has_expectation |= bool(expectations)
            for expected in expectations:
                if key in {'calls', 'notCalls'}:
                    _operation(expected, interfaces, vocabulary)
                elif key == 'agents' and (not re.fullmatch(r'[a-z0-9-]{1,64}', expected) or agents is not None and expected not in agents):
                    raise ResourceError(f'{identifier_case}: undeclared expected agent')
        if not has_expectation or set(expect.get('calls', [])) & set(expect.get('notCalls', [])):
            raise ResourceError(f'{identifier_case}: empty or contradictory grading contract')
        for observation in given['observations']:
            if not isinstance(observation, str) or not observation:
                raise ResourceError(f'{identifier_case}: invalid observation key')
            if observation.startswith('agent:'):
                role = observation[6:]
                if not re.fullmatch(r'[a-z0-9-]{1,64}', role) or agents is not None and role not in agents:
                    raise ResourceError(f'{identifier_case}: undeclared observed agent')
            elif '/' in observation:
                _operation(observation, interfaces, vocabulary)
    if not regression:
        raise ResourceError('missing authored regression case')


def validate_builder_skill(files: dict[str, bytes], metadata: dict,
                           capabilities: dict | None = None) -> None:
    """Validate the original builder entrypoint/role/case contract structurally.

    This cannot certify prose quality, permissions, source truth, runtime behavior
    or measured evaluations, and never updates status or approval records.
    """
    vocabulary = BUILDER_CAPABILITIES if capabilities is None else capabilities
    validate_resources(files, metadata)
    if metadata.get('schema') != 'talentsia-skill/v1' or not isinstance(metadata.get('id'), str) or not re.fullmatch(r'talentsia\.[a-z0-9-]+\.[a-z0-9-]+', metadata['id']):
        raise ResourceError('invalid builder skill identity/schema')
    if not isinstance(metadata.get('version'), str) or not re.fullmatch(r'\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?', metadata['version']):
        raise ResourceError('invalid builder skill version')
    if metadata.get('status') not in {'draft', 'released'}:
        raise ResourceError('invalid builder skill status')
    fields, body = _frontmatter(_text(files['SKILL.md'], 'SKILL.md'), 'SKILL.md')
    if set(fields) != {'name', 'description'} or not isinstance(fields['name'], str) or not re.fullmatch(r'[a-z0-9-]{1,64}', fields['name']) or metadata['id'].split('.')[-1] != fields['name']:
        raise ResourceError('builder frontmatter name or field mismatch')
    if not isinstance(fields['description'], str) or not 1 <= len(fields['description']) <= 1024 or fields['description'] != metadata.get('summary'):
        raise ResourceError('builder discovery description mismatch')
    opening = re.sub(r'\A\s*# [^\n]+\n', '', body).strip()
    intro = opening.split('\n\n')[0]
    if not intro.startswith('Read [the shared method](references/core.md) before proceeding.'):
        raise ResourceError('missing canonical shared-method entrypoint')
    headings = re.findall(r'^## (.+)$', body, re.M)
    order = ['When to use', 'Steps', 'Done when', 'Notes', 'A welcoming first turn', 'Handoffs']
    if headings[:3] != order[:3] or len(set(headings)) != len(headings) or any(h not in order for h in headings) or [order.index(h) for h in headings] != sorted(order.index(h) for h in headings):
        raise ResourceError('builder entrypoint sections missing, duplicated or out of order')
    sections = {}
    for index, heading in enumerate(headings):
        start = body.index('## '+heading) + len('## '+heading)
        end = body.index('## '+headings[index+1], start) if index+1 < len(headings) else len(body)
        sections[heading] = body[start:end].strip()
    if not sections['When to use'] or '\n\n' in sections['When to use']:
        raise ResourceError('When to use must be one paragraph')
    lines = [line for line in sections['Steps'].splitlines() if line.strip()]
    steps = []
    for index,line in enumerate(lines,1):
        match = re.fullmatch(r'(\d+)\. (.+)', line)
        if not match or match.group(1) != str(index) or len(match.group(2)) > 300:
            raise ResourceError('builder steps must be numbered and at most 300 characters')
        steps.append(match.group(2))
    if not 1 <= len(steps) <= 8:
        raise ResourceError('builder entrypoint requires one to eight steps')
    done = [line[2:] for line in sections['Done when'].splitlines() if line.startswith('- ')]
    if not done or any(not line.strip() for line in done) or done != metadata.get('verification'):
        raise ResourceError('Done when and canonical verification disagree')
    interfaces = _capabilities(metadata, vocabulary)
    declared_agents = set(metadata.get('subagents', []))
    for name,data in files.items():
        # Runtime references can explain placeholder grammar with metavariables;
        # executable entrypoint and role steps carry declarations to resolve.
        if name != 'SKILL.md' and not re.fullmatch(r'agents/[^/]+\.md', name):
            continue
        text = _text(data,name)
        for kind,target in re.findall(r'\{\{(tool|agent):([^}]+)\}\}', text):
            if kind == 'tool':
                _operation(target, interfaces, vocabulary)
            elif target not in declared_agents or name.startswith('agents/'):
                raise ResourceError(f'{name}: undeclared or recursive agent reference')
    for role in declared_agents:
        fields_role,_ = _frontmatter(_text(files[f'agents/{role}.md'],role),role)
        for tool in fields_role['tools']:
            _operation(tool,interfaces,vocabulary)
        if not fields_role['input'] or fields_role['output'].get('type') != 'object' or not fields_role['output'].get('required'):
            raise ResourceError('role requires nonempty input and object output with required fields')
    if 'evals/cases.json' not in files:
        raise ResourceError('missing authored evaluation cases')
    validate_builder_cases(_json(files['evals/cases.json'],'evals/cases.json'),metadata['id'],metadata,vocabulary)


def safe_path(name: str) -> str:
    """Validate an archive/resource member path without normalizing unsafe input."""
    if not isinstance(name, str) or not name or '\\' in name or any(ord(c) < 32 or 127 <= ord(c) <= 159 for c in name):
        raise ResourceError(f'unsafe resource path: {name!r}')
    parts = name.split('/')
    if name.startswith('/') or ':' in name or any(p in ('', '.', '..') or p.endswith((' ', '.')) for p in parts):
        raise ResourceError(f'unsafe resource path: {name!r}')
    if any(re.fullmatch(r'(?:con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?', p, re.I) for p in parts):
        raise ResourceError(f'unsafe portable resource path: {name!r}')
    if any(p.lower() in FORBIDDEN or p.lower().startswith('.env.') or p.lower().endswith(('.key', '.pem', '.pyc', '.sqlite')) or re.fullmatch(r'(?:run|runtime|work)[-_]record(?:s)?(?:\.[^.]+)?', p.lower()) for p in parts):
        raise ResourceError(f'forbidden member: {name}')
    return name


def _files(files):
    if not isinstance(files, dict) or len(files) > MAX_FILES:
        raise ResourceError('invalid or oversized resource set')
    total = 0
    for name, data in files.items():
        safe_path(name)
        if not isinstance(data, bytes):
            raise ResourceError(f'resource must be bytes: {name}')
        total += len(data)
    if total > MAX_BYTES:
        raise ResourceError('resource set too large')


def _text(data, name):
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ResourceError(f'invalid UTF-8: {name}') from exc


def _json(data, name):
    try:
        return json.loads(_text(data, name))
    except json.JSONDecodeError as exc:
        raise ResourceError(f'invalid JSON: {name}') from exc


def _schema(schema, location='schema'):
    """Check schema keyword shapes recursively; this is not an instance evaluator."""
    if isinstance(schema, bool):
        return
    if not isinstance(schema, dict):
        raise ResourceError(f'{location}: schema must be object or boolean')
    if '$ref' in schema and (not isinstance(schema['$ref'], str) or not schema['$ref']):
        raise ResourceError(f'{location}: invalid $ref')
    if 'type' in schema:
        types = schema['type'] if isinstance(schema['type'], list) else [schema['type']]
        if not types or any(t not in ('null', 'boolean', 'object', 'array', 'number', 'integer', 'string') for t in types):
            raise ResourceError(f'{location}: invalid type')
    if 'required' in schema:
        required = schema['required']
        if not isinstance(required, list) or any(not isinstance(x, str) for x in required) or len(set(required)) != len(required):
            raise ResourceError(f'{location}: invalid required')
        if schema.get('additionalProperties') is False and any(x not in schema.get('properties', {}) for x in required):
            raise ResourceError(f'{location}: required property cannot be supplied')
    for key in ('properties', 'patternProperties', '$defs', 'definitions', 'dependentSchemas'):
        if key in schema:
            if not isinstance(schema[key], dict):
                raise ResourceError(f'{location}: invalid {key}')
            for name, child in schema[key].items():
                _schema(child, f'{location}/{key}/{name}')
    for key in ('items', 'additionalProperties', 'contains', 'not', 'if', 'then', 'else', 'propertyNames', 'unevaluatedProperties', 'unevaluatedItems'):
        if key in schema:
            _schema(schema[key], f'{location}/{key}')
    for key in ('allOf', 'anyOf', 'oneOf', 'prefixItems'):
        if key in schema:
            if not isinstance(schema[key], list) or (key != 'prefixItems' and not schema[key]):
                raise ResourceError(f'{location}: invalid {key}')
            for child in schema[key]:
                _schema(child, f'{location}/{key}')
    for key in ('minItems', 'maxItems', 'minLength', 'maxLength', 'minProperties', 'maxProperties'):
        if key in schema and (type(schema[key]) is not int or schema[key] < 0):
            raise ResourceError(f'{location}: invalid {key}')
    for key in ('minItems', 'minLength', 'minProperties'):
        upper = key.replace('min', 'max')
        if key in schema and upper in schema and schema[key] > schema[upper]:
            raise ResourceError(f'{location}: contradictory {key}')
    if 'enum' in schema and (not isinstance(schema['enum'], list) or not schema['enum']):
        raise ResourceError(f'{location}: invalid enum')
    if 'pattern' in schema:
        try:
            re.compile(schema['pattern'])
        except (TypeError, re.error) as exc:
            raise ResourceError(f'{location}: invalid pattern') from exc


def _frontmatter(text, name):
    match = re.match(r'\A---\n(.*?)\n---(?:\n|$)', text, re.S)
    if not match:
        raise ResourceError(f'{name}: missing frontmatter')
    result = {}
    for line in match.group(1).splitlines():
        if ':' not in line:
            raise ResourceError(f'{name}: frontmatter requires one-line contract values')
        key, raw = line.split(':', 1)
        if key in result:
            raise ResourceError(f'{name}: duplicate field {key}')
        try:
            result[key] = json.loads(raw.strip())
        except json.JSONDecodeError:
            result[key] = raw.strip()
    return result, text[match.end():]


def _anchors(text):
    result = set(re.findall(r'<(?:a|\w+)\b[^>]*(?:id|name)=[\"\']([^\"\']+)', text))
    used = {}
    for heading in re.findall(r'^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$', text, re.M):
        heading = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', heading)
        slug = re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-')
        count = used.get(slug, 0)
        used[slug] = count + 1
        result.add(slug + (f'-{count}' if count else ''))
    return result


def _target(source, target, files, json_ref=False, schema_root=None):
    if not isinstance(target, str) or not target:
        raise ResourceError(f'{source}: invalid dependency target')
    target = target.strip()
    if target.startswith('<') and target.endswith('>'):
        target = target[1:-1]
    target = re.split(r'\s+[\"\']', target)[0]
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        if json_ref or parsed.scheme in ('file', 'javascript', 'data'):
            raise ResourceError(f'{source}: unresolved or unsafe dependency {target}')
        return
    resource = unquote(parsed.path)
    if '\\' in resource or resource.startswith('/'):
        raise ResourceError(f'{source}: unsafe link {target}')
    name = posixpath.normpath(posixpath.join(posixpath.dirname(source), resource)) if resource else source
    safe_path(name)
    if name not in files:
        raise ResourceError(f'{source}: missing resource {target}')
    if parsed.fragment:
        fragment = unquote(parsed.fragment)
        if json_ref:
            value = schema_root if schema_root is not None and name == source and not resource else _json(files[name], name)
            if fragment.startswith('/'):
                try:
                    for part in fragment[1:].split('/'):
                        part = part.replace('~1', '/').replace('~0', '~')
                        value = value[int(part)] if isinstance(value, list) else value[part]
                except (KeyError, IndexError, ValueError, TypeError) as exc:
                    raise ResourceError(f'{source}: missing schema pointer {target}') from exc
            elif not _has_anchor(value, fragment):
                raise ResourceError(f'{source}: missing schema anchor {target}')
        elif fragment not in _anchors(_text(files[name], name)):
            raise ResourceError(f'{source}: missing reference anchor {target}')


def _has_anchor(value, anchor):
    return isinstance(value, dict) and (value.get('$anchor') == anchor or any(_has_anchor(v, anchor) for v in value.values())) or isinstance(value, list) and any(_has_anchor(v, anchor) for v in value)


def _references(value, name, files, schema_root=None):
    if isinstance(value, dict):
        if '$ref' in value:
            _target(name, value['$ref'], files, json_ref=True, schema_root=schema_root)
        for child in value.values():
            _references(child, name, files, schema_root)
    elif isinstance(value, list):
        for child in value:
            _references(child, name, files, schema_root)


def validate_links(files: dict[str, bytes]) -> None:
    """Validate arbitrary folder dependencies without imposing a skill role contract."""
    _files(files)
    for name, data in files.items():
        if name.endswith('.json'):
            value = _json(data, name)
            if name.endswith('.schema.json'):
                _schema(value, name)
            _references(value, name, files)
        if name.endswith('.md'):
            text = _text(data, name)
            # Reference-style definitions and inline links/images both carry dependencies.
            targets = re.findall(r'!?\[[^\]]*\]\(([^)\n]+)\)', text)
            targets += re.findall(r'^ {0,3}\[[^\]]+\]:\s*(\S+)', text, re.M)
            for target in targets:
                _target(name, target, files)


def validate_resources(files: dict[str, bytes], metadata: dict) -> None:
    """Validate a skill-relative resource set and declared subagent contracts."""
    validate_links(files)
    if 'SKILL.md' not in files or not isinstance(metadata, dict):
        raise ResourceError('SKILL.md and canonical metadata are required')
    declarations = metadata.get('subagents', [])
    if not isinstance(declarations, list) or any(not isinstance(n, str) or not re.fullmatch(r'[a-z0-9-]{1,64}', n) for n in declarations) or len(set(declarations)) != len(declarations):
        raise ResourceError('invalid subagent declarations')
    skill = _text(files['SKILL.md'], 'SKILL.md')
    placeholders = set(re.findall(r'\{\{agent:([^}]+)\}\}', skill))
    if placeholders != set(declarations):
        raise ResourceError('declared subagents and literal agent placeholders disagree')
    role_files = {PurePosixPath(n).stem for n in files if re.fullmatch(r'agents/[^/]+\.md', n)}
    if role_files != set(declarations):
        raise ResourceError('role files and declarations disagree')
    capabilities = {c.split('@')[0] for c in metadata.get('requires', {}).get('capabilities', [])}
    for role in declarations:
        name = f'agents/{role}.md'
        if name not in files:
            raise ResourceError(f'missing declared role: {name}')
        fields, body = _frontmatter(_text(files[name], name), name)
        if set(fields) != {'name', 'description', 'tools', 'model', 'maxSteps', 'input', 'output'} or fields['name'] != role:
            raise ResourceError(f'{name}: invalid role fields/name')
        if not isinstance(fields['description'], str) or not fields['description'] or fields['model'] not in ('small-local', 'large-local', 'frontier'):
            raise ResourceError(f'{name}: invalid description/model')
        if type(fields['maxSteps']) is not int or not 1 <= fields['maxSteps'] <= 6:
            raise ResourceError(f'{name}: invalid maxSteps')
        if not isinstance(fields['input'], dict) or not isinstance(fields['output'], dict) or 'required' not in fields['output']:
            raise ResourceError(f'{name}: invalid input/output contract')
        _schema(fields['output'], name)
        _references(fields['output'], name, files, fields['output'])
        tools = fields['tools']
        if not isinstance(tools, list) or any(not isinstance(t, str) or '/' not in t or t.split('/')[0] not in capabilities for t in tools):
            raise ResourceError(f'{name}: role tools exceed declared capabilities')
        if body.count('## Steps') != 1 or body.count('## Done when') != 1:
            raise ResourceError(f'{name}: missing role sections')
        steps_text = body.split('## Steps', 1)[1].split('## Done when', 1)[0]
        steps = re.findall(r'^(\d+)\.\s+\S', steps_text, re.M)
        if steps != [str(i) for i in range(1, len(steps)+1)] or not 1 <= len(steps) <= fields['maxSteps'] or not re.search(r'^-\s+\S', body.split('## Done when', 1)[1], re.M):
            raise ResourceError(f'{name}: invalid steps/completion')


def archive(files: dict[str, bytes]) -> bytes:
    """Create an immutable deterministic ZIP from a validated byte mapping."""
    _files(files)
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name in sorted(files):
            entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = (stat.S_IFREG | 0o644) << 16
            entry.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(entry, files[name], compresslevel=9)
    return output.getvalue()


def verify_archive(path, sha: str) -> dict[str, bytes]:
    """Verify hash and safe members before returning bytes; never extract paths."""
    if not isinstance(sha, str) or not re.fullmatch(r'[0-9a-f]{64}', sha):
        raise ResourceError('invalid SHA256')
    blob = Path(path).read_bytes()
    if len(blob) > MAX_BYTES or hashlib.sha256(blob).hexdigest() != sha:
        raise ResourceError('archive checksum/size mismatch')
    result = {}
    try:
        with zipfile.ZipFile(io.BytesIO(blob)) as z:
            entries = z.infolist()
            if len(entries) > MAX_FILES or sum(e.file_size for e in entries) > MAX_BYTES:
                raise ResourceError('archive expansion limit exceeded')
            for entry in entries:
                safe_path(entry.filename)
                mode = entry.external_attr >> 16
                if entry.is_dir() or stat.S_ISLNK(mode) or (stat.S_IFMT(mode) not in (0, stat.S_IFREG)) or entry.flag_bits & 1:
                    raise ResourceError(f'unsafe archive member: {entry.filename}')
                if entry.filename in result:
                    raise ResourceError(f'duplicate archive member: {entry.filename}')
                result[entry.filename] = z.read(entry)
    except (zipfile.BadZipFile, RuntimeError) as exc:
        raise ResourceError('invalid archive') from exc
    _files(result)
    return result
