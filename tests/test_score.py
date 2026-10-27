import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import score


class ScoreTests(unittest.TestCase):
    def test_reference_timezone_weights(self):
        self.assertEqual(score.timezone_weight('Asia/Shanghai'), 1.0)
        self.assertEqual(score.timezone_weight('Asia/Hong_Kong'), 0.6)
        self.assertEqual(score.timezone_weight('America/Los_Angeles'), 0)
        self.assertIsNone(score.timezone_weight(None))

    def test_unknown_is_excluded_from_score(self):
        result = score.render_score({'timezone': None, 'offset_minutes': 480})
        self.assertIn('2.1 / 3 points', result)
        self.assertIn('not scored', result)
        self.assertIn('Not measured', result)

    def test_known_partial_score(self):
        result = score.render_score({'timezone': 'Asia/Hong_Kong', 'offset_minutes': 480})
        self.assertIn('16.5 / 27 points', result)
        self.assertIn('14.4 / 24', result)
        self.assertIn('2.1 / 3', result)
        self.assertNotIn('/ 100 points', result)

    def test_invalid_or_missing_override_is_not_guessed(self):
        self.assertIsNone(score.timezone_name({'TZ': 'America/NoSuchZone'}))
        self.assertIsNone(score.timezone_name({'TZ': ''}))
        self.assertEqual(score.timezone_name({'TZ': 'America/Los_Angeles'}), 'America/Los_Angeles')

    def test_real_process_override(self):
        script = str(Path(score.__file__))
        result = subprocess.run([sys.executable, script], env={**os.environ, 'TZ': 'America/Los_Angeles', 'NO_COLOR': '1'}, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('America/Los_Angeles', result.stdout)
        self.assertIn('0 / 27 points', result.stdout)
        self.assertRegex(result.stdout, r'UTC-0[78]:00')

    def test_no_network(self):
        with patch('socket.socket', side_effect=AssertionError('Unexpected network')):
            score.collect()


if __name__ == '__main__':
    unittest.main()
