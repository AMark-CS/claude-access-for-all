from pathlib import Path
import plistlib
import tempfile
import unittest
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import desktop_shortcut


class LauncherTests(unittest.TestCase):
    def test_builds_standalone_app_with_requested_environment(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle = desktop_shortcut.create_bundle(Path(tmp) / 'Claude Access Launcher.app', 'America/Los_Angeles', 'en_US.UTF-8')
            info = plistlib.loads((bundle / 'Contents/Info.plist').read_bytes())
            executable = bundle / 'Contents/MacOS' / info['CFBundleExecutable']
            self.assertTrue(executable.stat().st_mode & 0o111)
            script = executable.read_text()
            self.assertIn('TZ=America/Los_Angeles', script)
            self.assertIn('LANG=en_US.UTF-8', script)
            self.assertIn('/usr/bin/open -n -a Claude', script)
            self.assertTrue(info['LSUIElement'])

    def test_does_not_replace_existing_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'launcher.app'
            target.mkdir()
            marker = target / 'keep'
            marker.write_text('keep')
            with self.assertRaises(FileExistsError):
                desktop_shortcut.create_bundle(target, 'UTC', 'en_US.UTF-8')
            self.assertEqual(marker.read_text(), 'keep')


if __name__ == '__main__':
    unittest.main()
