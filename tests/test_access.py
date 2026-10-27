from datetime import date
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import access


class PrivacyTests(unittest.TestCase):
    def test_sensitive_values_never_appear(self):
        secret = 'private-value-that-must-never-leak'
        with patch.dict('os.environ', {name: secret for name in access.VARIABLES}, clear=True):
            result = access.doctor()
        report = json.dumps(result)
        self.assertNotIn(secret, report)
        self.assertTrue(all(result['environment_set'].values()))
        self.assertTrue(result['warnings'])

    def test_offline_doctor_does_not_launch_claude(self):
        with patch('subprocess.run', side_effect=AssertionError('Unexpected subprocess')):
            with patch('socket.socket', side_effect=AssertionError('Unexpected network')):
                with patch.dict('os.environ', {}, clear=True):
                    result = access.doctor()
        self.assertFalse(any(result['environment_set'].values()))


class CalendarTests(unittest.TestCase):
    def test_year_boundary_and_exclusive_end(self):
        content = access.reminder(date(2027, 1, 2), 3, date(2026, 12, 1))
        self.assertIn('DTSTART;VALUE=DATE:20261230\r\n', content)
        self.assertIn('DTEND;VALUE=DATE:20261231\r\n', content)
        self.assertIn('BEGIN:VALARM\r\n', content)
        self.assertIn('TRIGGER;RELATED=START:PT9H\r\n', content)
        self.assertNotIn('RRULE', content)
        self.assertNotIn('\n', content.replace('\r\n', ''))
        self.assertTrue(all(len(line.encode()) <= 75 for line in content.splitlines()))

    def test_leap_year(self):
        content = access.reminder(date(2028, 3, 1), 1, date(2028, 2, 1))
        self.assertIn('DTSTART;VALUE=DATE:20280229', content)

    def test_past_review_is_rejected(self):
        with self.assertRaises(ValueError):
            access.reminder(date(2026, 11, 1), 3, date(2026, 10, 30))

    def test_invalid_cli_input(self):
        script = str(Path(access.__file__))
        for args in [
            ['--renewal', '2027-02-30'],
            ['--renewal', '2027-12-01', '--days-before', '0'],
            ['--renewal', '2027-12-01', '--days-before', '366'],
            ['--renewal', '2027-12-01', '--days-before', 'oops'],
        ]:
            result = subprocess.run([sys.executable, script, 'reminder', *args], capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, b'')


if __name__ == '__main__':
    unittest.main()
