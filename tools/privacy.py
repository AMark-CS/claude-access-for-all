#!/usr/bin/env python3
"""Inspect and launch Claude clients with explicit, process-scoped locale settings."""
import argparse
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time

from report import render_audit

ROUTING = ('ANTHROPIC_BASE_URL', 'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'NO_PROXY',
           'http_proxy', 'https_proxy', 'all_proxy', 'no_proxy')
AUTH = ('ANTHROPIC_API_KEY', 'ANTHROPIC_AUTH_TOKEN')


def audit(environ=None):
    env = os.environ if environ is None else environ
    return {
        'scope': 'This terminal process only; not the browser, Desktop app, or server.',
        'timezone_override_set': bool(env.get('TZ')),
        'process_timezone_names': list(time.tzname),
        'locale_overrides_set': {key: bool(env.get(key)) for key in ('LANG', 'LC_ALL', 'LC_TIME')},
        'routing_overrides_set': {key: bool(env.get(key)) for key in ROUTING},
        'credential_overrides_set': {key: bool(env.get(key)) for key in AUTH},
        'claude_on_path': bool(shutil.which('claude')),
        'system': platform.system(),
        'limits': 'No network, IP lookup, application inspection, account check, or ban prediction.',
    }


def scoped_environment(source, timezone, locale):
    env = source.copy()
    env.update({'TZ': timezone, 'LANG': locale, 'LC_ALL': locale})
    return env


def validate_timezone(value):
    if value == 'UTC':
        return value
    if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_+-]*(/[A-Za-z0-9_+.-]+)+', value):
        raise argparse.ArgumentTypeError('Use UTC or an IANA timezone such as Europe/London.')
    path = Path('/usr/share/zoneinfo') / value
    if not path.is_file():
        raise argparse.ArgumentTypeError('Timezone is not present in /usr/share/zoneinfo.')
    return value


def validate_locale(value):
    if not re.fullmatch(r'[A-Za-z0-9_.@-]{1,64}', value):
        raise argparse.ArgumentTypeError('Use a locale such as en_US.UTF-8.')
    return value


def browser_command(browser, profile, language, timezone, locale):
    app = {'chrome': 'Google Chrome', 'edge': 'Microsoft Edge'}[browser]
    return ['/usr/bin/open', '-n', '-a', app, '--env', 'TZ=' + timezone,
            '--env', 'LANG=' + locale, '--env', 'LC_ALL=' + locale, '--args',
            '--user-data-dir=' + str(profile), '--lang=' + language, 'https://claude.ai/']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    diagnostic = sub.add_parser('audit', help='Show local signals without exposing secret values.')
    diagnostic.add_argument('--json', action='store_true', help='Output machine-readable JSON.')
    for name in ('cli', 'app', 'web'):
        command = sub.add_parser(name, help='Launch ' + name + ' with process-scoped settings.')
        command.add_argument('--timezone', type=validate_timezone, default='UTC')
        command.add_argument('--locale', type=validate_locale, default='en_US.UTF-8')
        if name == 'cli':
            command.add_argument('claude_args', nargs=argparse.REMAINDER)
        if name == 'app':
            command.add_argument('--app', default='Claude', help='macOS application name or absolute .app path.')
        if name == 'web':
            command.add_argument('--browser', choices=('chrome', 'edge'), default='chrome')
            command.add_argument('--profile', type=Path, help='Existing dedicated profile directory; omit for a new private directory.')
            command.add_argument('--language', default='en-US', type=validate_locale)
    args = parser.parse_args()
    if args.command == 'audit':
        result = audit()
        print(json.dumps(result, indent=2) if args.json else render_audit(result))
        return
    if sys.platform != 'darwin':
        parser.error('Launch commands require macOS.')
    env = scoped_environment(os.environ, args.timezone, args.locale)
    if args.command == 'cli':
        executable = shutil.which('claude')
        if not executable:
            parser.error('Claude Code was not found on PATH.')
        extra = args.claude_args
        if extra and extra[0] == '--':
            extra = extra[1:]
        print('Launching Claude Code with process-scoped TZ and locale; see /status for auth.', file=sys.stderr, flush=True)
        os.execve(executable, [executable, *extra], env)
    if args.command == 'app':
        command = ['/usr/bin/open', '-n', '-a', args.app,
                   '--env', 'TZ=' + args.timezone, '--env', 'LANG=' + args.locale,
                   '--env', 'LC_ALL=' + args.locale]
        print('Launching a new app instance; verify actual app behavior independently.', file=sys.stderr, flush=True)
    else:
        if args.profile:
            profile = args.profile.expanduser().resolve()
            if not profile.is_dir():
                parser.error('The dedicated browser profile directory must already exist.')
        else:
            profile = Path(tempfile.mkdtemp(prefix='claude-access-browser-'))
        command = browser_command(args.browser, profile, args.language, args.timezone, args.locale)
        print('Dedicated browser data directory: ' + str(profile), file=sys.stderr, flush=True)
        print('This directory may contain login data. Keep it private; remove it manually when finished.', file=sys.stderr, flush=True)
    try:
        result = subprocess.run(command, env=env, check=False)
    except OSError as error:
        parser.error(str(error))
    if result.returncode:
        raise SystemExit(result.returncode)


if __name__ == '__main__':
    main()
