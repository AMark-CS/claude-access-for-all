from pathlib import Path
import plistlib
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import autostart


class LoginItemTests(unittest.TestCase):
    def test_configuration_runs_once_with_scoped_environment(self):
        data = autostart.configuration()
        self.assertTrue(autostart.is_owned_config(data))
        self.assertEqual(data['ProgramArguments'][5], 'TZ=America/Los_Angeles')
        self.assertTrue(data['RunAtLoad'])
        self.assertNotIn('KeepAlive', data)
        self.assertEqual(data['LimitLoadToSessionType'], 'Aqua')

    def test_install_and_remove_without_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            path = autostart.agent_path(directory)
            autostart.install(path, 'America/Los_Angeles', 'en_US.UTF-8')
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertTrue(autostart.is_owned_config(plistlib.loads(path.read_bytes())))
            with self.assertRaises(FileExistsError):
                autostart.install(path, 'UTC', 'en_US.UTF-8')
            with patch.object(autostart, 'loaded', return_value=False):
                self.assertTrue(autostart.uninstall(path))
            self.assertFalse(path.exists())

    def test_unrecognized_file_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'agent.plist'
            contents = plistlib.dumps({'Label': 'other.service', 'ProgramArguments': ['/bin/true']})
            path.write_bytes(contents)
            with self.assertRaises(ValueError):
                autostart.uninstall(path)
            self.assertEqual(path.read_bytes(), contents)

    def test_disable_preserves_file_if_unload_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'agent.plist'
            autostart.install(path, 'UTC', 'en_US.UTF-8')
            with patch.object(autostart, 'loaded', return_value=True), patch.object(autostart.subprocess, 'run') as run:
                run.return_value.returncode = 1
                with self.assertRaises(RuntimeError):
                    autostart.uninstall(path)
            self.assertTrue(path.exists())


if __name__ == '__main__':
    unittest.main()
