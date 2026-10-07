"""Check the public distribution inventory, links, metadata and accidental secrets."""
import argparse
import ast
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ('ai-video-qms','ai-video-fullchain','shortdrama-production-qa','shortdrama-micro-performance')
PRIVATE_DIRS = {'.git','data','private','outputs','.venv','node_modules','__pycache__','.pytest_cache'}
PATH_RE = re.compile(r'(?i)\b[A-Z]:[\\/]|/mnt/[a-z]/|/Users/[A-Za-z]|/home/[A-Za-z]')
CREDENTIAL_RE = re.compile(r'(?:ghp_|github_pat_|sk-proj-)[A-Za-z0-9_]{20,}')
LINK_RE = re.compile(r'!?\[[^\]]*\]\(([^)\n]+)\)')


def check(root=ROOT, tracked=False):
    root = Path(root).resolve()
    issues, files = [], []
    if tracked:
        result = subprocess.run(['git','ls-files','-z'],cwd=root,capture_output=True)
        if result.returncode:
            raise ValueError('Cannot list Git distribution files')
        files = [root/name for name in result.stdout.decode('utf-8').split('\0') if name]
    else:
        files = [p for p in root.rglob('*') if p.is_file() and not any(x in PRIVATE_DIRS for x in p.relative_to(root).parts)]
    for path in files:
        relative = path.relative_to(root)
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            issues.append('Escaping/symlink file: '+relative.as_posix()); continue
        if any(p in PRIVATE_DIRS for p in relative.parts) or path.name in ('.runtime.json','.env') or path.suffix in ('.mp4','.mov','.wav','.mp3','.sqlite','.db','.pem','.key','.zip'):
            issues.append('Private/generated distribution file: '+relative.as_posix()); continue
        if path.suffix not in ('.md','.json','.jsonl','.js','.py','.toml','.yaml','.yml'):
            continue
        try:
            text = path.read_text(encoding='utf-8-sig')
        except UnicodeDecodeError:
            issues.append('Non-UTF8 text: '+relative.as_posix()); continue
        if PATH_RE.search(text):
            issues.append('Host path leaked: '+relative.as_posix())
        if CREDENTIAL_RE.search(text):
            issues.append('Possible credential: '+relative.as_posix())
        if path.suffix == '.py':
            try: ast.parse(text)
            except SyntaxError as exc: issues.append(f'Syntax: {relative}: {exc}')
        if path.suffix == '.json':
            try: json.loads(text)
            except ValueError as exc: issues.append(f'JSON: {relative}: {exc}')
        if path.suffix == '.md':
            for target in LINK_RE.findall(text):
                target = target.split(' ',1)[0].strip('<>')
                if '://' in target or target.startswith(('#','mailto:')):
                    continue
                target = target.split('#')[0]
                if target and not (path.parent/target).resolve().exists():
                    issues.append(f'Broken local link: {relative}: {target}')
    registry=json.loads((root/'standards/registry.json').read_text(encoding='utf-8'))
    docs={d['id']:d for d in registry['documents']}
    facets={f for d in docs.values() if d['kind']=='sop' and d['status']=='released' for f in d.get('facets',[])}
    wiki=json.loads((root/'wiki/index.json').read_text(encoding='utf-8'))
    if wiki.get('schema_version') != 1 or len(wiki.get('tasks',{})) != 8:
        issues.append('Invalid task navigation schema')
    for task,row in wiki.get('tasks',{}).items():
        if any(x not in facets for x in row['facets']): issues.append('Unknown Wiki facet: '+task)
        if any(x not in docs for x in row['templates']): issues.append('Unknown Wiki template: '+task)
        if any(x not in SKILLS for x in row['skills']): issues.append('Unknown bundled Skill: '+task)
        page=(root/row['page']).resolve()
        if not page.is_relative_to(root) or not page.is_file(): issues.append('Invalid Wiki path: '+task)
    for name in SKILLS:
        path=root/'skills'/name/'SKILL.md'
        if not path.is_file(): issues.append('Missing Skill: '+name); continue
        body=path.read_text(encoding='utf-8')
        if not body.startswith('---\n') or not re.search('^name: '+re.escape(name)+'$',body,re.M) or not re.search(r'^description:\s*\S',body,re.M):
            issues.append('Invalid Skill frontmatter: '+name)
        for rel in ('agents/openai.yaml','scripts/run.py'):
            if not (path.parent/rel).is_file(): issues.append('Missing Skill dependency: '+name+'/'+rel)
    return {'ok': not issues,'files_checked':len(files),'documents':len(docs),'profiles':len(registry['profiles']),'skills':len(SKILLS),'issues':issues,'validation':'distribution structure and automated pattern scan; not a guarantee of rights or audiovisual quality'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--tracked',action='store_true')
    args=p.parse_args()
    result=check(args.root,args.tracked)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(0 if result['ok'] else 1)
