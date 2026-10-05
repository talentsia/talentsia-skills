"""Generate a readable indexed reference; does not deploy or install anything."""
import argparse,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PLUGIN=ROOT/'plugins/talentsia-do'
ORDER=['clear-my-head','organize-my-work','plan-my-day','move-forward','prepare','do-with-me','follow-through','make-room','resume','review']
REFS={'core.md':'shared-method','operating-instructions.md':'authority-and-delegation','review-and-planning.md':'review-and-planning','methodology-sources.md':'methodology-sources'}
def rewrite(text):
    for name,anchor in REFS.items():
        text=re.sub(r'\]\((?:references/)?'+re.escape(name)+r'\)','](#'+anchor+')',text)
    return text

def generate():
    version=json.loads((PLUGIN/'plugin.json').read_text())['version']
    parts=[f'# Talentsia Do {version} — Project reference / Referência de Projeto',
        ('Local candidate / Candidata local. ' if '-' in version else '') + 'This reference adapts instructions for a private Project; it is not a native plugin installation. Real mobile behavior has not been tested. Personal records belong in user-chosen private storage. No automatic memory, synchronization, monitoring or external permission is supplied.',
        'Use PT/EN as requested. Read [Shared method](#shared-method) and the [workflow](#clear-my-head) matching the request before proceeding. Read [Review and planning](#review-and-planning) for weekly/broader review, project uncertainty or horizon conflicts; [Authority and delegation](#authority-and-delegation) for those questions. If a section cannot be accessed, request it and disclose partial coverage. Keep one canonical record and the same IDs.',
        '## Index / Índice\n\n'+ '\n'.join(f'- [{label}](#{anchor})' for label,anchor in [('Shared method / Método comum','shared-method'),('Authority and delegation / Autoridade e delegação','authority-and-delegation'),('Review and planning / Revisão e planejamento','review-and-planning')]+[(n.replace('-',' ').title(),n) for n in ORDER]+[('Methodology sources / Fontes','methodology-sources')])]
    for name in ['core.md','operating-instructions.md','review-and-planning.md']:
        parts.append('<a id="'+REFS[name]+'"></a>\n\n'+rewrite((PLUGIN/'references'/name).read_text()))
    for name in ORDER:
        body=(PLUGIN/'skills'/name/'SKILL.md').read_text().split('---',2)[2].strip()
        parts.append('<a id="'+name+'"></a>\n\n'+rewrite(body))
    parts.append('<a id="methodology-sources"></a>\n\n'+rewrite((PLUGIN/'references/methodology-sources.md').read_text()))
    return '\n\n'.join(parts)+'\n'
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--output',required=True);args=a.parse_args()
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(generate())
    print('Generated local reference:',out)
