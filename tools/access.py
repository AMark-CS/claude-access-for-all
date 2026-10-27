#!/usr/bin/env python3
"""Offline environment checks and a one-time subscription review calendar."""
import argparse
from datetime import date, datetime, timedelta, timezone
import json
import os
import platform
import shutil
import sys
import uuid

from report import render_doctor

VARIABLES = (
    'ANTHROPIC_API_KEY', 'ANTHROPIC_AUTH_TOKEN', 'ANTHROPIC_BASE_URL',
    'CLAUDE_CODE_USE_BEDROCK', 'CLAUDE_CODE_USE_VERTEX', 'CLAUDE_CODE_USE_FOUNDRY',
    'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'NO_PROXY',
    'http_proxy', 'https_proxy', 'all_proxy', 'no_proxy',
    'NODE_EXTRA_CA_CERTS', 'NODE_TLS_REJECT_UNAUTHORIZED',
)


def doctor():
    """Report presence only; never serialize environment values or local paths."""
    present = {name: bool(os.environ.get(name)) for name in VARIABLES}
    warnings = []
    if platform.system() != 'Darwin':
        warnings.append('This guide targets macOS; this machine uses another OS.')
    if not shutil.which('claude'):
        warnings.append('Claude Code is not on PATH. See docs/macos-quickstart.md.')
    if any(present[n] for n in ('ANTHROPIC_API_KEY', 'ANTHROPIC_AUTH_TOKEN', 'ANTHROPIC_BASE_URL')):
        warnings.append('Authentication or endpoint overrides are set. Verify /status before use.')
    if present['ALL_PROXY'] or present['all_proxy']:
        warnings.append('ALL_PROXY is set; do not assume Claude Code uses it. Check the network guide.')
    if present['NODE_TLS_REJECT_UNAUTHORIZED']:
        warnings.append('A TLS validation override is set. Review it privately; keep verification enabled.')
    return {
        'mode': 'offline; no network requests; no account eligibility check',
        'system': platform.system(),
        'macos_version': platform.mac_ver()[0] if platform.system() == 'Darwin' else None,
        'architecture': platform.machine(),
        'claude_on_path': bool(shutil.which('claude')),
        'environment_set': present,
        'warnings': warnings,
        'limitations': 'Does not inspect system proxies, Claude settings, credentials, or billing state.',
    }


def parse_date(value):
    try:
        parsed = date.fromisoformat(value)
        if parsed.isoformat() != value:
            raise ValueError
        return parsed
    except ValueError:
        raise argparse.ArgumentTypeError('Use a valid date in YYYY-MM-DD format.')


def days_before(value):
    try:
        number = int(value)
        if not 1 <= number <= 365:
            raise ValueError
        return number
    except ValueError:
        raise argparse.ArgumentTypeError('Choose a whole number from 1 to 365.')


def reminder(renewal, lead, today=None):
    """Generate a bounded ASCII RFC 5545 event; all dates are local calendar dates."""
    today = today or date.today()
    review = renewal - timedelta(days=lead)
    if review < today:
        raise ValueError('Review date is in the past. Choose a later renewal or shorter lead time.')
    end = review + timedelta(days=1)
    lines = [
        'BEGIN:VCALENDAR', 'VERSION:2.0',
        'PRODID:-//Claude Access for All//Subscription Review//EN',
        'CALSCALE:GREGORIAN', 'BEGIN:VEVENT',
        'UID:' + str(uuid.uuid4()) + '@claude-access-for-all',
        'DTSTAMP:' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'),
        'DTSTART;VALUE=DATE:' + review.strftime('%Y%m%d'),
        'DTEND;VALUE=DATE:' + end.strftime('%Y%m%d'),
        'SUMMARY:Review Claude subscription renewal',
        'DESCRIPTION:Check billing provider and renewal date before any charge.',
        'TRANSP:TRANSPARENT', 'BEGIN:VALARM', 'ACTION:DISPLAY',
        'TRIGGER;RELATED=START:PT9H',
        'DESCRIPTION:Review Claude subscription in your billing provider.',
        'END:VALARM', 'END:VEVENT', 'END:VCALENDAR', '',
    ]
    return '\r\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    diagnostic = commands.add_parser('doctor', help='Print an offline environment report.')
    diagnostic.add_argument('--json', action='store_true', help='Output machine-readable JSON.')
    calendar = commands.add_parser('reminder', help='Print a one-time .ics calendar to stdout.')
    calendar.add_argument('--renewal', type=parse_date, required=True)
    calendar.add_argument('--days-before', type=days_before, default=3)
    args = parser.parse_args()
    if args.command == 'doctor':
        result = doctor()
        print(json.dumps(result, indent=2) if args.json else render_doctor(result))
    else:
        try:
            content = reminder(args.renewal, args.days_before)
        except (ValueError, OverflowError) as exc:
            parser.error(str(exc))
        sys.stdout.buffer.write(content.encode('ascii'))


if __name__ == '__main__':
    main()
