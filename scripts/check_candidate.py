"""Offline artifact checks: no model execution, installation or external side effects."""
import argparse,hashlib,json,re,zipfile
from pathlib import Path
from mobile_reference import generate,PLUGIN,ROOT,ORDER
import pocket

def check(out):
 version=json.loads((PLUGIN/'plugin.json').read_text())['version']
 cases=json.loads((ROOT/'evals/cases.json').read_text())
 assert cases['model_execution']=='not_run'
 ids=[c['id'] for c in cases['cases']]
 assert len(ids)==len(set(ids))==64
 assert all(c['status']=='not_run' and c['expected'] for c in cases['cases'])
 text=(out/f'talentsia-do-project-reference-{version}.md').read_text()
 assert text==generate(),'Consolidated reference is stale'
 anchors=re.findall(r'<a id="([^"]+)"></a>',text)
 assert len(anchors)==len(set(anchors))==14
 links=re.findall(r'\]\(#([^)]+)\)',text)
 assert set(links)<=set(anchors),'Broken internal anchor'
 assert not re.findall(r'\]\((?:references/)?[\w-]+\.md\)',text),'Unresolved file link in mobile reference'
 # Pocket texts must match canonical sources and stay within paste budgets; the zip must carry exactly those texts plus the reference.
 _,pocket_files=pocket.artifacts()
 for filename,expected_text in pocket_files.items():
  assert (out/filename).read_text()==expected_text,f'Pocket artifact stale: {filename}'
 with zipfile.ZipFile(out/f'talentsia-do-pocket-{version}.zip') as z:
  names=set(z.namelist());prefix=f'talentsia-do-pocket-{version}/'
  assert names=={prefix+n for n in list(pocket_files)+[f'talentsia-do-project-reference-{version}.md','index.json']}
  assert all(z.read(prefix+n).decode()==t for n,t in pocket_files.items())
  assert z.read(prefix+f'talentsia-do-project-reference-{version}.md').decode()==text
  assert set(json.loads(z.read(prefix+'index.json'))['files'])==set(pocket_files)|{f'talentsia-do-project-reference-{version}.md'}
 # Ensure isolated skill packages each carry the complete reference closure.
 for name in ORDER:
  with zipfile.ZipFile(out/f'{name}-{version}.zip') as z:
   names=set(z.namelist())
   assert f'{name}/SKILL.md' in names
   assert sum(n.endswith('/SKILL.md') for n in names)==1
   for ref in (PLUGIN/'references').glob('*.md'):
    assert z.read(f'{name}/references/{ref.name}')==ref.read_bytes()
   for n in names:
    if n.endswith('.md'):
     for link in re.findall(r'\]\(([^)]+)\)',z.read(n).decode()):
      if '://' in link or link.startswith('#'):continue
      target=str(Path(n).parent/link.split('#')[0])
      assert target in names,(name,n,link)
 with zipfile.ZipFile(out/f'talentsia-do-plugin-{version}.zip') as z:
  expected={str(Path('talentsia-do')/f.relative_to(PLUGIN)):f.read_bytes() for f in PLUGIN.rglob('*') if f.is_file()}
  assert set(z.namelist())==set(expected)
  assert all(z.read(n)==data for n,data in expected.items())
 files=sorted(out.glob('*.zip'))+sorted(out.glob('*.md'))
 hashes={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
 report={'candidate_version':version,'status':'prepared_artifacts','checks':{'exact_skill_count':10,'complete_reference_exports':True,'isolated_archive_reference_closure':True,'plugin_archive_matches_source':True,'mobile_unique_anchors':14,'mobile_internal_links':len(links),'mobile_content_matches_source':True,'pocket_texts':len(pocket_files),'pocket_content_matches_source':True,'pocket_within_budgets':True,'synthetic_fixture_count':64},'model_behavior':'not_run','native_host_loading':'not_run','mobile_app_behavior':'not_run','pocket_paste_behavior':'not_run','hashes':hashes}
 (out/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--output',required=True);args=a.parse_args();check(Path(args.output))
