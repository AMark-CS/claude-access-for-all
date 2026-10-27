import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import privacy


class PrivacyToolTests(unittest.TestCase):
    def test_audit_redacts_routing_and_credentials(self):
        marker = 'private-proxy-user-password-or-token'
        env = {name: marker for name in (*privacy.ROUTING, *privacy.AUTH, 'LANG', 'TZ')}
        report = privacy.audit(env)
        self.assertNotIn(marker, json.dumps(report))
        self.assertTrue(all(report['routing_overrides_set'].values()))
        self.assertTrue(all(report['credential_overrides_set'].values()))

    def test_scoped_environment_does_not_mutate_source_and_preserves_auth(self):
        original = {'TZ': 'Asia/Hong_Kong', 'ANTHROPIC_API_KEY': 'secret', 'HTTPS_PROXY': 'proxy'}
        result = privacy.scoped_environment(original, 'UTC', 'en_US.UTF-8')
        self.assertEqual(original['TZ'], 'Asia/Hong_Kong')
        self.assertEqual(result['TZ'], 'UTC')
        self.assertEqual(result['LANG'], 'en_US.UTF-8')
        self.assertEqual(result['LC_ALL'], 'en_US.UTF-8')
        self.assertEqual(result['ANTHROPIC_API_KEY'], 'secret')
        self.assertEqual(result['HTTPS_PROXY'], 'proxy')

    def test_web_command_sets_launch_environment_and_isolated_profile(self):
        result = privacy.browser_command('chrome', Path('/tmp/example profile'), 'en-US', 'UTC', 'en_US.UTF-8')
        self.assertIn('--user-data-dir=/tmp/example profile', result)
        self.assertIn('TZ=UTC', result)
        self.assertEqual(result[-1], 'https://claude.ai/')
        self.assertLess(result.index('--env'), result.index('--args'))

    def test_launch_is_explicit_and_audit_offline(self):
        with patch('subprocess.run', side_effect=AssertionError('unexpected process')):
            with patch('socket.socket', side_effect=AssertionError('unexpected network')):
                privacy.audit({})

    def test_cli_rejects_unknown_timezone_without_launch(self):
        script = str(Path(privacy.__file__))
        result = subprocess.run([sys.executable, script, 'cli', '--timezone', 'Mars/Olympus'], capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn(b'Timezone', result.stderr)
        self.assertEqual(result.stdout, b'')


if __name__ == '__main__':
    unittest.main()
