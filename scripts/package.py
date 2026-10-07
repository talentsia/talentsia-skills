"""Validate and export Talentsia Do without runtime dependencies or network calls."""
import argparse,json,re,shutil,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PLUGIN=ROOT/'plugins/talentsia-do'
NAMES={'clear-my-head','organize-my-work','plan-my-day','move-forward','prepare','do-with-me','follow-through','make-room','resume','review'}

def validate():
    skills=list((PLUGIN/'skills').glob('*/SKILL.md'))
    assert {p.parent.name for p in skills}==NAMES and len(skills)==10,'Expected exactly ten skills'
    manifest=json.loads((PLUGIN/'plugin.json').read_text())
    compat=json.loads((PLUGIN/'.claude-plugin/plugin.json').read_text())
    catalog=json.loads((ROOT/'.agents/plugins/marketplace.json').read_text())
    claude=json.loads((ROOT/'.claude-plugin/marketplace.json').read_text())
    version=manifest['version']
    assert manifest['name']==compat['name']=='talentsia-do'
    assert compat['version']==claude['plugins'][0]['version']==version
    assert catalog['plugins'][0]['name']=='talentsia-do'
    assert catalog['plugins'][0]['source']=={'source':'git-subdir','url':'https://github.com/talentsia/talentsia-skills.git','path':'./plugins/talentsia-do','ref':'v'+version}
    assert manifest['extensions']['com.openai']['interface']['websiteURL']=='https://skills.talentsia.com'
    assert manifest['homepage']==compat['homepage']=='https://skills.talentsia.com'
    for p in skills:
        parts=p.read_text().split('---',2);assert len(parts)==3
        fields=dict(line.split(': ',1) for line in parts[1].strip().splitlines())
        assert set(fields)=={'name','description'}
        assert fields['name']==p.parent.name and re.fullmatch('[a-z0-9-]{1,64}',fields['name'])
        description=json.loads(fields['description']);assert isinstance(description,str) and 1<=len(description)<=1024
        metadata=(p.parent/'agents/openai.yaml').read_text().splitlines();assert metadata[0]=='interface:'
        ui={line.strip().split(': ',1)[0]:json.loads(line.strip().split(': ',1)[1]) for line in metadata[1:]}
        assert 25<=len(ui['short_description'])<=64 and '$'+p.parent.name in ui['default_prompt']
        assert '[the shared method](references/core.md)' in parts[2]
        for source in (p for p in (PLUGIN/'references').iterdir() if p.suffix in {'.md','.json'}):
            assert (p.parent/'references'/source.name).read_bytes()==source.read_bytes(),'Reference export stale'
    for p in ROOT.rglob('*'):
        if '.git' in p.parts or not p.is_file():continue
        assert not p.is_symlink(),p
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
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='/tmp/talentsia-do-release');args=parser.parse_args()
    for skill in (PLUGIN/'skills').iterdir():
        if (skill/'SKILL.md').is_file():
            for p in (p for p in (PLUGIN/'references').iterdir() if p.suffix in {'.md','.json'}):shutil.copy2(p,skill/'references'/p.name)
    version,skills=validate();out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True)
    assert not out.is_relative_to(ROOT),'Archives must be outside repository'
    archive(PLUGIN,out/f'talentsia-do-plugin-{version}.zip')
    with zipfile.ZipFile(out/f'talentsia-do-plugin-{version}.zip') as z:
        assert len([n for n in z.namelist() if n.endswith('/SKILL.md')])==10
    print(f'PASS static discovery/frontmatter/metadata/references/archive: ten skills, one plugin, {version}. Behavior evals not executed.')
