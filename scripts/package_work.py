"""Validate and export Talentsia Work without network calls or credentials.

Talentsia Work differs from Talentsia Do in two ways that this script checks:
it ships code (a standard-library MCP client), and it uses Codex's own
`.codex-plugin/plugin.json` because Codex reads MCP servers only from that
manifest, and ignores it entirely when a root `plugin.json` is present.
"""
import argparse,ast,hashlib,json,os,re,shutil,subprocess,sys,tempfile,tomllib,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PLUGIN=ROOT/'plugins/talentsia-work'
NAMES=['connect-seat','start-work','deliver-work','keep-promises','hand-over','what-needs-me']
ROLES=['content-designer','content-writer','executive-assistant','software-engineer']
TOOLS=15
STDLIB={'__future__','argparse','base64','hashlib','hmac','importlib','json','os','re','secrets','shutil','stat','sys','time','urllib','pathlib'}
TAG='talentsia-work-v{}'

def frontmatter(path):
    parts=path.read_text().split('---',2);assert len(parts)==3 and parts[0]=='',path
    return dict(line.split(': ',1) for line in parts[1].strip().splitlines() if not line.startswith(' ')),parts[2]

def validate():
    codex=json.loads((PLUGIN/'.codex-plugin/plugin.json').read_text())
    claude=json.loads((PLUGIN/'.claude-plugin/plugin.json').read_text())
    version=codex['version']
    assert not (PLUGIN/'plugin.json').exists(),'a root plugin.json makes Codex ignore .codex-plugin and its MCP server'
    assert codex['name']==claude['name']=='talentsia-work' and claude['version']==version
    assert codex['homepage']==claude['homepage']==codex['interface']['websiteURL']=='https://skills.talentsia.com'
    for key in ('logo','composerIcon'):assert (PLUGIN/codex['interface'][key]).is_file()
    assert codex['skills']=='./skills/' and codex['mcpServers']=='./codex-mcp.json'
    cmcp=json.loads((PLUGIN/'codex-mcp.json').read_text())['mcpServers']['talentsia-work']
    assert cmcp['cwd']=='.' and (PLUGIN/cmcp['args'][0]).is_file()
    assert claude['mcpServers']['talentsia-work']['args']==['${CLAUDE_PLUGIN_ROOT}/server/mcp_server.py']
    assert 'userConfig' not in claude,'userConfig is rejected by Claude Code releases still in use'
    for name in ('.agents/plugins/marketplace.json','.claude-plugin/marketplace.json'):
        entry=[p for p in json.loads((ROOT/name).read_text())['plugins'] if p['name']=='talentsia-work']
        assert len(entry)==1,name
        if name.startswith('.agents'):
            assert entry[0]['source']=={'source':'git-subdir','url':'https://github.com/talentsia/talentsia-skills.git','path':'./plugins/talentsia-work','ref':TAG.format(version)}
        else:
            assert entry[0]['source']=='./plugins/talentsia-work' and entry[0]['version']==version
    server=(PLUGIN/'server/mcp_server.py').read_text()
    assert f'VERSION = "{version}"' in server,'server VERSION differs from the plugin version'
    skills=sorted((PLUGIN/'skills').glob('*/SKILL.md'))
    assert [p.parent.name for p in skills]==sorted(NAMES),'Expected exactly the six Talentsia Work skills'
    protocol=(PLUGIN/'references/seat-protocol.md').read_bytes()
    for p in skills:
        fields,body=frontmatter(p);assert set(fields)=={'name','description'} and fields['name']==p.parent.name
        description=json.loads(fields['description']);assert 1<=len(description)<=1024
        assert '[the seat protocol](references/seat-protocol.md)' in body and '`how_this_seat_works`' in body
        assert (p.parent/'references/seat-protocol.md').read_bytes()==protocol,'Reference export stale'
        ui=(p.parent/'agents/openai.yaml').read_text().splitlines();assert ui[0]=='interface:'
        ui={l.strip().split(': ',1)[0]:json.loads(l.strip().split(': ',1)[1]) for l in ui[1:]}
        assert 25<=len(ui['short_description'])<=64 and '$'+p.parent.name in ui['default_prompt']
    agents=sorted((PLUGIN/'agents').glob('*.md'))
    assert [p.stem for p in agents]==ROLES
    for p in agents:
        fields,body=frontmatter(p);assert set(fields)=={'name','description'} and fields['name']==p.stem
        assert '`how_this_seat_works`' in body and '## What I could not establish' in body
    for p in (PLUGIN/'server').glob('*.py'):
        tree=ast.parse(p.read_text())
        for node in ast.walk(tree):
            if isinstance(node,(ast.Import,ast.ImportFrom)):
                names=[a.name for a in node.names] if isinstance(node,ast.Import) else [node.module or '']
                for n in names:
                    assert n.split('.')[0] in STDLIB|{'talentsia_agent'},f'{p.name} imports {n}: the seat client is standard library only'
    return version

def smoke():
    """Handshake, tool list and a refused call, with no credentials anywhere."""
    with tempfile.TemporaryDirectory() as home:
        env={**os.environ,'HOME':home,'TALENTSIA_AGENTS_FILE':'','TALENTSIA_AGENT_ID':'','TALENTSIA_AGENT_KEY':'','TALENTSIA_WORKSPACE':''}
        lines=[{'jsonrpc':'2.0','id':1,'method':'initialize','params':{}},{'jsonrpc':'2.0','method':'notifications/initialized'},
               {'jsonrpc':'2.0','id':2,'method':'tools/list'},{'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'my_tasks','arguments':{}}}]
        out=subprocess.run([sys.executable,str(PLUGIN/'server/mcp_server.py'),'--as','${user_config.seat}'],input='\n'.join(map(json.dumps,lines))+'\n',
                           capture_output=True,text=True,env=env,timeout=30,check=True).stdout.splitlines()
        answers={m['id']:m['result'] for m in map(json.loads,out)}
        assert answers[1]['serverInfo']['name']=='talentsia-work'
        tools=answers[2]['tools'];assert len(tools)==TOOLS
        assert all(len(t['description'])>=40 and t['inputSchema']['type']=='object' for t in tools)
        assert answers[3]['isError'] and 'no agent configured' in answers[3]['content'][0]['text']
        for harness in ('codex','claude'):
            subprocess.run([sys.executable,str(PLUGIN/'server/setup_seat.py'),f'{harness}-agent','--seat','designer','--role','content-designer'],
                           env={**env,'CODEX_HOME':f'{home}/codex','CLAUDE_CONFIG_DIR':f'{home}/claude'},capture_output=True,check=True,timeout=30)
        agent=tomllib.loads(Path(home,'codex/agents/designer.toml').read_text())
        assert agent['mcp_servers']['talentsia']['args'][1:]==['--as','designer'] and agent['developer_instructions']
        text=Path(home,'claude/agents/designer.md').read_text();assert 'mcpServers:' in text and '"--as", "designer"' in text
    for p in (PLUGIN/'server').glob('__pycache__'):shutil.rmtree(p)
    return len(tools)

def archive(folder,path):
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(folder.rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:z.write(p,Path(folder.name)/p.relative_to(folder))
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in z.namelist())
        assert not any(n.endswith(('.env','.sqlite','.pem','.pyc','agents.json')) for n in z.namelist())
        expected={str(Path(folder.name)/f.relative_to(folder)) for f in folder.rglob('*') if f.is_file() and '__pycache__' not in f.parts}
        assert set(z.namelist())==expected

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='/tmp/talentsia-work-release');args=parser.parse_args()
    for skill in (PLUGIN/'skills').iterdir():
        if (skill/'SKILL.md').is_file():
            (skill/'references').mkdir(exist_ok=True);shutil.copy2(PLUGIN/'references/seat-protocol.md',skill/'references/seat-protocol.md')
    version=validate();tools=smoke()
    cases=json.loads((ROOT/'evals/talentsia-work-cases.json').read_text())
    assert cases['model_execution']=='not_run' and len({c['id'] for c in cases['cases']})==len(cases['cases'])>=12
    assert {c['expected_skill'] for c in cases['cases']}>=set(NAMES)
    out=Path(args.output).resolve();assert not out.is_relative_to(ROOT),'Archives must be outside repository'
    out.mkdir(parents=True,exist_ok=True)
    for stale in out.glob('talentsia-work-*'):stale.unlink()
    zip_path=out/f'talentsia-work-plugin-{version}.zip';archive(PLUGIN,zip_path)
    files=[zip_path]+sorted((PLUGIN/'server').glob('*.py'))
    sums=''.join(f'{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.name}\n' for f in files)
    (out/f'talentsia-work-{version}.SHA256SUMS').write_text(sums)
    report={'candidate_version':version,'tag':TAG.format(version),'status':'prepared_artifacts',
            'checks':{'skills':len(NAMES),'role_agents':len(ROLES),'mcp_tools':tools,'stdlib_only_client':True,'mcp_handshake':True,
                      'unconfigured_call_refused':True,'agent_writers':['codex','claude'],'synthetic_fixture_count':len(cases['cases'])},
            'model_behavior':'not_run','native_host_loading':'not_run','live_workspace':'not_run','signature':'not_signed','sha256':sums.splitlines()}
    (out/f'talentsia-work-{version}.checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print(f'PASS Talentsia Work {version}: six skills, four role agents, {tools} MCP tools, stdlib-only client, archive and checksums. Behavior evals not executed; artifacts not signed.')
