"""Copy complete Skill folders and connect them to this cloned repository."""
import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAMES = ('ai-video-qms', 'ai-video-fullchain', 'shortdrama-production-qa', 'shortdrama-micro-performance')


def install(target, root=ROOT):
    root, target = Path(root).resolve(), Path(target).resolve()
    if not (root/'qms-project.json').is_file():
        raise ValueError('Not an AI video QMS repository')
    if target.is_relative_to(root/'skills'):
        raise ValueError('Cannot install into the source Skill folders')
    for name in NAMES:
        if not (root/'skills'/name/'SKILL.md').is_file():
            raise ValueError('Missing bundled Skill: '+name)
        if (target/name).exists():
            raise ValueError('Existing Skill will not be overwritten: '+str(target/name))
    target.mkdir(parents=True, exist_ok=True)
    created = []
    try:
        for name in NAMES:
            destination = target/name
            shutil.copytree(root/'skills'/name, destination, ignore=shutil.ignore_patterns('__pycache__', '.runtime.json', '*.pyc'))
            created.append(destination)
            (destination/'.runtime.json').write_text(json.dumps({'repository_root': str(root)}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    except Exception:
        # Only remove the directories just created by this failed installation.
        for destination in created:
            resolved = destination.resolve()
            if resolved.parent != target or resolved.name not in NAMES:
                raise ValueError('Created Skill path escaped the installation target; refusing cleanup')
            shutil.rmtree(resolved)
        raise
    return {'installed': list(NAMES), 'target': str(target), 'repository_root': str(root)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', required=True, type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(install(args.target), ensure_ascii=False, indent=2))
    except (ValueError, OSError) as exc:
        parser.exit(1, str(exc)+'\n')
