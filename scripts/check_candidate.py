"""Offline artifact checks: no model execution, installation or external side effects."""
import argparse,hashlib,json,re,zipfile
from pathlib import Path
from skill_file import generate,PLUGIN,ROOT,ORDER

def check(out):
 version=json.loads((PLUGIN/'plugin.json').read_text())['version']
 assert (ROOT/'LICENSE').is_file() and (ROOT/'SKILLS-LICENSE').is_file() and (ROOT/'CODE-LICENSE').is_file() and (ROOT/'NOTICE.md').is_file()
 license_index=(ROOT/'LICENSE').read_text()
 assert 'SKILLS-LICENSE' in license_index and 'CODE-LICENSE' in license_index
 cases=json.loads((ROOT/'evals/cases.json').read_text())
 assert cases['model_execution']=='not_run'
 ids=[c['id'] for c in cases['cases']]
 assert len(ids)==len(set(ids))==64
 assert all(c['status']=='not_run' and c['expected'] for c in cases['cases'])
 # The single skill file must match canonical sources, contain every skill and both references, and the upload zip must carry exactly it.
 _,text=generate()
 assert (out/f'SKILL-talentsia-do-{version}.md').read_text()==text,'Skill file is stale'
 assert text.startswith('---\nname: talentsia-do\n')
 for name in ORDER:assert f'(`{name}`)' in text,name
 assert '## Review and planning (reference)' in text and '## Authority and delegation (reference)' in text
 with zipfile.ZipFile(out/f'talentsia-do-skill-{version}.zip') as z:
  assert z.namelist()==['talentsia-do/SKILL.md'] and z.read('talentsia-do/SKILL.md').decode()==text
 with zipfile.ZipFile(out/f'talentsia-do-plugin-{version}.zip') as z:
  expected={str(Path('talentsia-do')/f.relative_to(PLUGIN)):f.read_bytes() for f in PLUGIN.rglob('*') if f.is_file()}
  assert set(z.namelist())==set(expected)
  assert all(z.read(n)==data for n,data in expected.items())
 files=sorted(out.glob('*.zip'))+sorted(out.glob('*.md'))
 assert {f.name for f in files}=={f'talentsia-do-plugin-{version}.zip',f'talentsia-do-skill-{version}.zip',f'SKILL-talentsia-do-{version}.md'},'Unexpected release artifacts'
 hashes={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
 report={'candidate_version':version,'status':'prepared_artifacts','checks':{'exact_skill_count':10,'complete_reference_exports':True,'plugin_archive_matches_source':True,'skill_file_matches_source':True,'skill_file_characters':len(text),'skill_zip_matches_file':True,'synthetic_fixture_count':64},'model_behavior':'not_run','native_host_loading':'not_run','skill_file_behavior':'not_run','hashes':hashes}
 (out/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--output',required=True);args=a.parse_args();check(Path(args.output))
