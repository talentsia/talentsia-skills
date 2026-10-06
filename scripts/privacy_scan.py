"""Offline public-artifact hygiene checks, not a comprehensive secret detector."""
import argparse,re,subprocess,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATTERNS=[
 re.compile(r'(?i)["\']key["\']\s*:\s*["\'][0-9a-f]{64,}["\']'),
 re.compile(r'TALENTSIA_AGENT_KEY\s*=\s*["\']?[0-9a-fA-F]{64,}'),
 re.compile(r'(?<![A-Za-z0-9])/(?:Users|home)/[^\s"\']+'),
 re.compile(r'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|sk-(?:proj-)?[A-Za-z0-9_-]{25,})'),
 re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
 re.compile(r'(?i)Bearer\s+[A-Za-z0-9._=-]{20,}'),
 re.compile(r'(?i)(?:luiz@luizdasilva\.com|dev@talentsia\.com|appgprj_[a-z0-9]+|page[_-][a-f0-9]{24,})')]
FORBIDDEN={'installation-receipt.json','fresh-session-source-check.json','source-changes.patch','ROLLBACK.md','READINESS.md','.env','.app.json','agents.json','.talentsia'}

def inspect(name,data):
 assert not any(part in FORBIDDEN or part in {'local-marketplace','_context'} for part in Path(name).parts),name
 assert not name.endswith(('.pem','.sqlite','.db','.pyc')),name
 try:text=data.decode('utf-8')
 except UnicodeDecodeError:return
 for pattern in PATTERNS:
  assert not pattern.search(text),f'Potential private material in {name}; inspect locally (content withheld)'

def scan(out=None):
 files=subprocess.run(['git','ls-files','-z','--cached','--others','--exclude-standard'],cwd=ROOT,capture_output=True,check=True).stdout.decode().split('\0')
 for name in filter(None,files):
  p=ROOT/name
  assert not p.is_symlink(),name
  if p.is_file():inspect(name,p.read_bytes())
 count=0
 if out:
  for p in Path(out).iterdir():
   if p.suffix=='.zip':
    with zipfile.ZipFile(p) as z:
     for name in z.namelist():
      if not name.endswith('/'):inspect(name,z.read(name));count+=1
   elif p.suffix in {'.md','.json','.txt'}:inspect(p.name,p.read_bytes());count+=1
 print(f'PASS bounded hygiene scan: source inventory and {count} asset entries; no matched private paths, known identifiers, credential patterns or excluded artifacts. Not a comprehensive secret audit.')
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--output');args=a.parse_args();scan(args.output)
