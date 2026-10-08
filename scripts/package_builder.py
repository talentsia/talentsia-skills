"""Validate and export Talentsia Skill Builder without runtime dependencies or network calls."""
import argparse,json,re,shutil,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PLUGIN=ROOT/'plugins/talentsia-skill-builder'
NAMES={'scope-a-skill','draft-a-skill','review-a-skill','test-a-skill','export-a-pack'}
ROLES={'case-author','step-writer','contract-checker','red-team-reviewer','worker-rehearsal','pack-assembler'}
SECTIONS=['When to use','Steps','Done when','Notes','A welcoming first turn','Handoffs']
ROLE_SECTIONS=['Before anything','Craft','Must not','Return']
REFERENCES={'core.md','skill-contract.md','skill-template.md','subagent-contract.md','eval-design.md','capabilities.md','review-checklist.md','export-layout.md'}

def frontmatter(path):
    parts=path.read_text().split('---',2);assert len(parts)==3,path
    fields=dict(line.split(': ',1) for line in parts[1].strip().splitlines())
    return fields,parts[2]

def headings(body):
    return [line[3:].strip() for line in body.splitlines() if line.startswith('## ')]

def validate():
    skills=sorted((PLUGIN/'skills').glob('*/SKILL.md'))
    assert {p.parent.name for p in skills}==NAMES and len(skills)==5,'Expected exactly five skills'
    manifest=json.loads((PLUGIN/'plugin.json').read_text())
    compat=json.loads((PLUGIN/'.claude-plugin/plugin.json').read_text())
    version=manifest['version']
    assert manifest['name']==compat['name']=='talentsia-skill-builder' and compat['version']==version
    assert manifest['homepage']==compat['homepage']=='https://skills.talentsia.com'
    assert not (PLUGIN/'talentsia-package.json').exists() and not list(PLUGIN.rglob('skill.json')),'Builder targets harnesses; keep it out of the Edge validators'
    assert {p.name for p in (PLUGIN/'references').iterdir()}==REFERENCES
    roles=sorted((PLUGIN/'agents').glob('*.md'));assert {p.stem for p in roles}==ROLES
    for p in roles:
        fields,body=frontmatter(p)
        assert set(fields)=={'name','description'} and fields['name']==p.stem,p
        assert headings(body)==ROLE_SECTIONS,(p,headings(body))
    for p in skills:
        fields,body=frontmatter(p)
        assert set(fields)=={'name','description'}
        assert fields['name']==p.parent.name and re.fullmatch('[a-z0-9-]{1,64}',fields['name'])
        description=json.loads(fields['description']);assert isinstance(description,str) and 1<=len(description)<=1024
        assert headings(body)==SECTIONS,(p,headings(body))
        steps=re.findall(r'^(\d+)\. (.*)$',body.split('## Steps')[1].split('## Done when')[0],re.M)
        assert 1<=len(steps)<=8 and [int(n) for n,_ in steps]==list(range(1,len(steps)+1)),p
        assert all(len(s)<=300 for _,s in steps),(p,'step over 300 characters')
        assert '[the shared method](references/core.md)' in body
        for role in re.findall(r'`([a-z-]+)` role',body):assert role in ROLES,(p,role)
        placeholders=set(re.findall(r'<[A-Za-z][^<>\n]*>',body))-{'<name>'}
        assert not placeholders,(p,placeholders)
        metadata=(p.parent/'agents/openai.yaml').read_text().splitlines();assert metadata[0]=='interface:'
        ui={line.strip().split(': ',1)[0]:json.loads(line.strip().split(': ',1)[1]) for line in metadata[1:]}
        assert 25<=len(ui['short_description'])<=64 and '$'+p.parent.name in ui['default_prompt']
        for source in (PLUGIN/'references').iterdir():
            assert (p.parent/'references'/source.name).read_bytes()==source.read_bytes(),'Reference export stale'
    for p in PLUGIN.rglob('*'):
        if not p.is_file():continue
        assert not p.is_symlink() and p.suffix in {'.md','.json','.yaml','.svg',''},p
        if p.suffix=='.json':json.loads(p.read_text())
        if p.suffix=='.md':
            for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
                if '://' in link or link.startswith('#'):continue
                target=(p.parent/link.split('#')[0]).resolve()
                assert target.is_relative_to(ROOT) and target.is_file(),(p,link)
    for key in ['logo','composerIcon']:
        assert (PLUGIN/manifest['extensions']['com.openai']['interface'][key]).is_file()
    return version,skills

def archive(folder,path):
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(folder.rglob('*')):
            if p.is_file():z.write(p,Path(folder.name)/p.relative_to(folder))
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in z.namelist())
        assert not any('/.git/' in n or n.endswith(('.env','.sqlite','.pem')) for n in z.namelist())

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='/tmp/talentsia-skill-builder-release');args=parser.parse_args()
    for skill in (PLUGIN/'skills').iterdir():
        if (skill/'SKILL.md').is_file():
            (skill/'references').mkdir(exist_ok=True)
            for p in (PLUGIN/'references').iterdir():shutil.copy2(p,skill/'references'/p.name)
    version,skills=validate();out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True)
    assert not out.is_relative_to(ROOT),'Archives must be outside repository'
    archive(PLUGIN,out/f'talentsia-skill-builder-plugin-{version}.zip')
    with zipfile.ZipFile(out/f'talentsia-skill-builder-plugin-{version}.zip') as z:
        assert len([n for n in z.namelist() if n.endswith('/SKILL.md')])==5
    print(f'PASS static discovery/frontmatter/roles/references/archive: five skills, six roles, {version}. Behavior evals not executed.')
