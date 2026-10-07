import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tools import install_skills, shot_plan

SOURCE_ROOT = Path(__file__).resolve().parents[1]


class OutputBoundaryTests(unittest.TestCase):
    def test_direct_shot_bundle_output_stays_inside_project(self):
        with TemporaryDirectory() as tmp:
            sandbox = Path(tmp).resolve()
            repo = sandbox / 'repo'
            standards = repo / 'standards'
            standards.mkdir(parents=True)
            outside = sandbox / 'escaped'
            with self.assertRaisesRegex(ValueError, 'inside the project root'):
                shot_plan.write_bundle_output(standards, outside, 'body', {}, {})
            self.assertFalse(outside.exists())
            for name in ('standards', 'tools', 'skills', 'wiki', 'docs', '.git'):
                with self.assertRaisesRegex(ValueError, 'controlled directories'):
                    shot_plan.write_bundle_output(standards, repo/name/'bundle', 'body', {}, {})
            output = repo/'data'/'example'
            shot_plan.write_bundle_output(standards, output, 'body', {}, {})
            self.assertEqual((output/'bundle.md').read_text(encoding='utf-8'), 'body')
            with self.assertRaises(FileExistsError):
                shot_plan.write_bundle_output(standards, output, 'new', {}, {})
            self.assertEqual((output/'bundle.md').read_text(encoding='utf-8'), 'body')

    def test_install_complete_skills_and_run_from_unicode_project(self):
        with TemporaryDirectory(prefix='ai-video-install-') as tmp:
            sandbox = Path(tmp).resolve()
            target = sandbox/'短剧 示例 项目'/'.agents'/'skills'
            result = install_skills.install(target, SOURCE_ROOT)
            self.assertEqual(result['installed'], list(install_skills.NAMES))
            environment = dict(os.environ)
            environment.pop('AI_VIDEO_QMS_HOME', None)
            for name in install_skills.NAMES:
                skill = target/name
                self.assertTrue((skill/'SKILL.md').is_file())
                self.assertTrue((skill/'agents'/'openai.yaml').is_file())
                self.assertTrue((skill/'references').is_dir())
                runtime = json.loads((skill/'.runtime.json').read_text(encoding='utf-8'))
                self.assertEqual(Path(runtime['repository_root']).resolve(), SOURCE_ROOT)
                run = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(skill/'scripts'/'run.py'), 'doctor'], cwd=target.parent.parent, env=environment, capture_output=True, encoding='utf-8')
                self.assertEqual(run.returncode, 0, run.stderr)
                self.assertTrue(json.loads(run.stdout)['ok'])
            marker = target/install_skills.NAMES[0]/'keep.txt'
            marker.write_text('existing user data', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Existing Skill'):
                install_skills.install(target, SOURCE_ROOT)
            self.assertEqual(marker.read_text(encoding='utf-8'), 'existing user data')


if __name__ == '__main__':
    unittest.main()
