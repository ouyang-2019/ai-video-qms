"""Seal an edited public standards edition. Run only as an explicit release step."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def seal(root):
    root = Path(root).resolve()
    standards = root / 'standards'
    registry = json.loads((standards/'registry.json').read_text(encoding='utf-8'))
    def sha(file):
        path = (standards/file).resolve()
        if not path.is_relative_to(standards):
            raise ValueError('Manifest path escapes standards')
        return hashlib.sha256(path.read_bytes()).hexdigest()
    release = {
        'schema_version': 1, 'version': registry['version'],
        'registry_sha256': sha('registry.json'), 'sources_sha256': sha('sources.json'),
        'documents': [dict(id=d['id'], file=d['file'], version=d['version'], sha256=sha(d['file']))
                      for d in registry['documents'] if d['status'] == 'released']
    }
    supplement_files = ['relations.json'] + [p.relative_to(standards).as_posix() for p in sorted((standards/'metadata').rglob('*.json'))]
    supplement = {'schema_version': 1, 'files': [{'file': f, 'sha256': sha(f)} for f in supplement_files]}
    for name, data in [('release-content.json', release), ('supplement-content.json', supplement)]:
        (standards/name).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
    return {'sealed_documents': len(release['documents']), 'supplements': len(supplement['files'])}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    print(json.dumps(seal(args.root)))
