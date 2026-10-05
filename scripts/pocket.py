"""Generate pasteable pocket artifacts for clients without plugin installation; no deployment or network."""
import argparse,hashlib,json,re,zipfile
from pathlib import Path
from mobile_reference import PLUGIN,ROOT,ORDER
SITE='https://skills.talentsia.com'
# Character budgets keep each artifact pasteable on a phone; the Review card carries the weekly-review reference.
BUDGETS={'start':8000,'project-instructions':8000,'card':8500,'card-review':17000}
DEEP_NOTE=('Deeper references named above (review-and-planning, operating-instructions) are not included in this card. '
 'Apply the shared method, say that the deeper reference was unavailable, and suggest the full Project reference or installed plugin when it matters.')

def version():return json.loads((PLUGIN/'plugin.json').read_text())['version']
def method():
    text=(PLUGIN/'pocket/method.md').read_text().strip()
    assert text.startswith('# ')
    return '## Shared method / Método comum\n\n'+text.split('\n',1)[1].strip()
PASTE_CHAT='_Paste this entire text as the first message of a new chat, then say what is on your mind. / Cole este texto inteiro como a primeira mensagem de uma nova conversa e depois diga o que está na sua cabeça._'
PASTE_PROJECT='_Paste this entire text into the Project instructions field and upload the reference file to the same Project. / Cole este texto inteiro no campo de instruções do Projeto e envie o arquivo de referência para o mesmo Projeto._'
def frontmatter(name):
    parts=(PLUGIN/'skills'/name/'SKILL.md').read_text().split('---',2)
    fields=dict(line.split(': ',1) for line in parts[1].strip().splitlines())
    return json.loads(fields['description']),parts[2].strip()
def ui(name):
    lines=(PLUGIN/'skills'/name/'agents/openai.yaml').read_text().splitlines()[1:]
    return {l.strip().split(': ',1)[0]:json.loads(l.strip().split(': ',1)[1]) for l in lines}
def plain_links(text):return re.sub(r'\[([^\]]+)\]\((?:references/)?[\w-]+\.md\)',r'\1',text)
def body_without_preamble(name):
    _,body=frontmatter(name)
    paragraphs=body.split('\n\n')
    assert paragraphs[1].startswith('Read [the shared method]'),name
    return plain_links('\n\n'.join(paragraphs[2:]))

def menu():
    rows=[]
    for name in ORDER:
        description,_=frontmatter(name)
        rows.append(f"- **{ui(name)['display_name']}** (`{name}`): {description}")
    return '\n'.join(rows)

def footer(v):
    return (f'Talentsia Do {v} pocket edition, {SITE}. This pasted text is instructions, not an installed plugin, a saved record or a storage service. '
     'Independent implementation; no third-party endorsement or guaranteed result is claimed.')

def start(v):
    return '\n\n'.join([f'# Talentsia Do {v} — start here / comece aqui',PASTE_CHAT,method(),'## The ten workflows / Os dez fluxos',menu(),
     '## How to begin / Como começar',
     'Infer the workflow from what the user says next, or ask one short question offering two or three fitting workflows. '
     'If the user names a workflow, apply it. Do not ask for setup, storage or deadlines before being useful; start from the user\'s own words and existing records when supplied. '
     'Keep all ten in mind for handoffs, and tell the user which workflow you are applying.',footer(v)])+'\n'

def card(name,v):
    display=ui(name)['display_name'];description,_=frontmatter(name)
    prompt=ui(name)['default_prompt'].replace('$'+name,display)
    parts=[f'# Talentsia Do {v} — {display} / pocket card',f'_{description}_',PASTE_CHAT,method(),f'## {display}',body_without_preamble(name)]
    if name=='review':
        parts+=['## Review and planning',plain_links((PLUGIN/'references/review-and-planning.md').read_text().strip())]
    elif 'review-and-planning' in parts[-1] or 'operating-instructions' in parts[-1]:
        parts.append(DEEP_NOTE)
    parts+=[f'## Start / Começar\nExample request: “{prompt}” Apply {display} to what the user sends next.',footer(v)]
    return '\n\n'.join(parts)+'\n'

def project_instructions(v):
    ref=f'talentsia-do-project-reference-{v}.md'
    return '\n\n'.join([f'# Talentsia Do {v} — Project instructions / Instruções do Projeto',PASTE_PROJECT,method(),
     '## Reference file / Arquivo de referência',
     f'This Project includes the file `{ref}`. Before applying a workflow, read its “Shared method” section and the section named after the chosen workflow; '
     'read “Review and planning” for weekly or broader review or an unclear project, and “Authority and delegation” for ownership or delegation questions. '
     'If the file cannot be opened, say so and work from these instructions alone without claiming the deeper method was applied. '
     'Personal records belong in the user\'s own storage or in this Project\'s chats marked not saved; the reference file is not a record.',
     '## The ten workflows / Os dez fluxos',menu(),footer(v)])+'\n'

def artifacts():
    v=version();out={f'talentsia-do-start-{v}.md':('start',start(v)),f'talentsia-do-project-instructions-{v}.md':('project-instructions',project_instructions(v))}
    for name in ORDER:out[f'talentsia-do-card-{name}-{v}.md']=('card-review' if name=='review' else 'card',card(name,v))
    for filename,(kind,text) in out.items():
        assert len(text)<=BUDGETS[kind],f'{filename} exceeds {BUDGETS[kind]} characters ({len(text)})'
        assert not re.findall(r'\]\((?:references/)?[\w-]+\.md\)',text),f'Unresolved file link in {filename}'
    return v,{k:t for k,(_,t) in out.items()}

def write(out):
    v,files=artifacts();out.mkdir(parents=True,exist_ok=True)
    for filename,text in files.items():(out/filename).write_text(text)
    reference=out/f'talentsia-do-project-reference-{v}.md'
    assert reference.is_file(),'Generate the Project reference first'
    index={'version':v,'site':SITE,'files':{}}
    with zipfile.ZipFile(out/f'talentsia-do-pocket-{v}.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in [out/f for f in files]+[reference]:
            data=p.read_bytes();z.writestr(f'talentsia-do-pocket-{v}/{p.name}',data)
            index['files'][p.name]={'characters':len(data.decode()),'sha256':hashlib.sha256(data).hexdigest()}
        z.writestr(f'talentsia-do-pocket-{v}/index.json',json.dumps(index,indent=2)+'\n')
    return v,files

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--output',required=True);args=a.parse_args()
    v,files=write(Path(args.output).resolve())
    sizes=', '.join(f'{k.split("-"+v)[0].replace("talentsia-do-","")}={len(t)}' for k,t in files.items())
    print(f'Generated pocket edition {v}: {len(files)} texts + zip. Characters: {sizes}')
