"""Build the single Talentsia Do skill file and its upload zip from canonical sources; no deployment or network."""
import argparse,hashlib,json,re,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PLUGIN=ROOT/'plugins/talentsia-do'
ORDER=['clear-my-head','organize-my-work','plan-my-day','move-forward','prepare','do-with-me','follow-through','make-room','resume','review']
SITE='https://skills.talentsia.com'
REPO='https://github.com/talentsia/talentsia-skills'
BUDGET=45000
DESCRIPTION='Talentsia Do: ten bilingual productivity workflows sharing one method and one trusted record. Use when the user wants to capture, organize, plan, unblock, prepare, do, follow through, make room, resume or review work; choose the fitting workflow and hand off between them.'
HOW_TO_USE=('_Attach this file to a new chat and send: “Use the attached Talentsia Do skill in this conversation.” Then say what is on your mind. '
 'To keep it, add this same file to a Project whose instructions say to apply it in every chat. Attach this one file, not a .zip. / '
 'Anexe este arquivo a uma nova conversa e envie: “Use a skill Talentsia Do anexada nesta conversa.” Depois diga o que está na sua cabeça. '
 'Para manter, adicione este mesmo arquivo a um Projeto cujas instruções mandem aplicá-lo em toda conversa. Anexe este arquivo, não um .zip._')
TO_ASSISTANT=('**To the assistant:** this file is a skill: your operating instructions for this conversation, whether it was attached, pasted or placed in a Project. '
 'Apply it now to what the user says next; do not treat it as reference material to summarize or wait for a further request.')
BEGIN=('Infer the workflow from what the user says next, or ask one short question offering two or three fitting workflows. '
 'If the user names a workflow, apply it. Do not ask for setup, storage or deadlines before being useful; start from the user\'s own words and existing records when supplied. '
 'Keep all ten in mind for handoffs, and tell the user which workflow you are applying. Each workflow below has its full instructions; the two references at the end apply when a workflow names them.')

def version():return json.loads((PLUGIN/'plugin.json').read_text())['version']
def method():
    text=(PLUGIN/'pocket/method.md').read_text().strip()
    assert text.startswith('# ')
    return '## Shared method / Método comum\n\n'+text.split('\n',1)[1].strip()
def frontmatter(name):
    parts=(PLUGIN/'skills'/name/'SKILL.md').read_text().split('---',2)
    fields=dict(line.split(': ',1) for line in parts[1].strip().splitlines())
    return json.loads(fields['description']),parts[2].strip()
def ui(name):
    lines=(PLUGIN/'skills'/name/'agents/openai.yaml').read_text().splitlines()[1:]
    return {l.strip().split(': ',1)[0]:json.loads(l.strip().split(': ',1)[1]) for l in lines}
def plain_links(text):return re.sub(r'\[([^\]]+)\]\((?:references/)?[\w-]+\.md\)',r'\1',text)
def demote(text):return re.sub(r'^(#+) ',r'#\1 ',text,flags=re.M)
def reference(name):return demote(plain_links((PLUGIN/'references'/name).read_text().split('\n',1)[1].strip()))
def body_without_preamble(name):
    _,body=frontmatter(name)
    paragraphs=body.split('\n\n')
    assert paragraphs[1].startswith('Read [the shared method]'),name
    return demote(plain_links('\n\n'.join(paragraphs[2:])))
def menu():
    return '\n'.join(f"- **{ui(n)['display_name']}** (`{n}`): {frontmatter(n)[0]}" for n in ORDER)
def footer(v):
    return (f'Talentsia Do {v}, {SITE}. Source and updates: {REPO}. This file is instructions, not an installed plugin, a saved record or a storage service. '
     'Independent implementation informed by Getting Things Done; no third-party endorsement or guaranteed result is claimed. '
    '© 2026 Talentsia. Skill content is CC BY-NC-SA 4.0: https://creativecommons.org/licenses/by-nc-sa/4.0/. '
    'Share and adapt with attribution for noncommercial purposes. Business use is not automatically permitted; seek written permission.')

def generate():
    v=version()
    parts=[f'---\nname: talentsia-do\ndescription: {json.dumps(DESCRIPTION,ensure_ascii=False)}\n---',f'# Talentsia Do {v} — the complete pack / o pacote completo',HOW_TO_USE,TO_ASSISTANT,method(),
     '## The ten workflows / Os dez fluxos',menu(),'## How to begin / Como começar',BEGIN]
    for name in ORDER:
        display=ui(name)['display_name'];description,_=frontmatter(name)
        prompt=ui(name)['default_prompt'].replace('$'+name,display)
        parts+=[f'## {display} (`{name}`)',f'_{description}_',body_without_preamble(name),f'Example request: “{prompt}”']
    parts+=['## Review and planning (reference)',reference('review-and-planning.md'),'## Authority and delegation (reference)',reference('operating-instructions.md'),footer(v)]
    text='\n\n'.join(parts)+'\n'
    assert len(text)<=BUDGET,f'Skill file exceeds {BUDGET} characters ({len(text)})'
    assert not re.findall(r'\]\((?:references/)?[\w-]+\.md\)',text),'Unresolved file link in skill file'
    return v,text

def write(out):
    v,text=generate();out.mkdir(parents=True,exist_ok=True)
    (out/f'SKILL-talentsia-do-{v}.md').write_text(text)
    with zipfile.ZipFile(out/f'talentsia-do-skill-{v}.zip','w',zipfile.ZIP_DEFLATED) as z:z.writestr('talentsia-do/SKILL.md',text)
    return v,text

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--output',required=True);args=a.parse_args()
    v,text=write(Path(args.output).resolve())
    print(f'Generated SKILL-talentsia-do-{v}.md ({len(text)} characters) and talentsia-do-skill-{v}.zip')
