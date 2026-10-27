#!/usr/bin/env python3
"""Manage an opt-in per-user login launch for Claude Desktop on macOS."""
import argparse
import os
from pathlib import Path
import plistlib
import subprocess
import sys

from privacy import validate_locale, validate_timezone

LABEL = 'org.claudeaccess.desktop-login'


def agent_path(home=None):
    return Path.home() / 'Library' / 'LaunchAgents' / (LABEL + '.plist') if home is None else Path(home) / 'Library' / 'LaunchAgents' / (LABEL + '.plist')


def configuration(timezone='America/Los_Angeles', locale='en_US.UTF-8'):
    return {
        'Label': LABEL,
        'ProgramArguments': ['/usr/bin/open', '-g', '-a', 'Claude',
                             '--env', 'TZ=' + timezone, '--env', 'LANG=' + locale,
                             '--env', 'LC_ALL=' + locale],
        'RunAtLoad': True,
        'LimitLoadToSessionType': 'Aqua',
    }


def is_owned_config(data):
    if not isinstance(data, dict) or data.get('Label') != LABEL:
        return False
    args = data.get('ProgramArguments')
    if not isinstance(args, list) or len(args) != 10:
        return False
    if args[:4] != ['/usr/bin/open', '-g', '-a', 'Claude'] or args[4::2] != ['--env'] * 3:
        return False
    if not all(isinstance(x, str) for x in args):
        return False
    return (args[5].startswith('TZ=') and args[7].startswith('LANG=') and
            args[9].startswith('LC_ALL=') and data.get('RunAtLoad') is True)


def install(path, timezone, locale):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    content = plistlib.dumps(configuration(timezone, locale))
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, 'wb') as file:
            file.write(content)
    except BaseException:
        path.unlink(missing_ok=True)
        raise
    return path


def read_config(path):
    try:
        with Path(path).open('rb') as file:
            data = plistlib.load(file)
    except (OSError, ValueError, plistlib.InvalidFileException):
        return None
    return data if is_owned_config(data) else None


def loaded():
    result = subprocess.run(['/bin/launchctl', 'print', f'gui/{os.getuid()}/{LABEL}'],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    return result.returncode == 0


def uninstall(path):
    path = Path(path)
    if not path.exists():
        return False
    if read_config(path) is None:
        raise ValueError('Existing file is not a recognized Claude Access login item; it was not removed.')
    if loaded():
        result = subprocess.run(['/bin/launchctl', 'bootout', f'gui/{os.getuid()}/{LABEL}'],
                                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, check=False)
        if result.returncode != 0 and loaded():
            raise RuntimeError('Could not unload the login item; it remains enabled. Check macOS Login Items.')
    path.unlink()
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    enable = commands.add_parser('enable', help='Install a login item; it starts at the next login.')
    enable.add_argument('--timezone', type=validate_timezone, default='America/Los_Angeles')
    enable.add_argument('--locale', type=validate_locale, default='en_US.UTF-8')
    commands.add_parser('status', help='Check installation and whether the item is loaded.')
    commands.add_parser('disable', help='Remove the login item; leave Claude running.')
    args = parser.parse_args()
    if sys.platform != 'darwin':
        parser.error('Login startup requires macOS.')
    path = agent_path()
    if args.command == 'enable':
        try:
            install(path, args.timezone, args.locale)
        except FileExistsError:
            parser.error('Login item already exists. Run status; disable it before changing settings.')
        except OSError as error:
            parser.error(str(error))
        print('Enabled for next macOS login:', path)
        print('After login, requests Claude Desktop with timezone:', args.timezone)
        print('It does not inject settings into an already-running Claude instance.')
    elif args.command == 'status':
        if not path.exists():
            print('Login item: not installed')
            return
        data = read_config(path)
        if data is None:
            print('Login item: unrecognized file; no changes made', file=sys.stderr)
            raise SystemExit(1)
        print('Login item: installed')
        print('Loaded in this login session:', 'yes' if loaded() else 'no (takes effect on next login)')
        print('Requested timezone:', data['ProgramArguments'][5][3:])
        print('Requested locale:', data['ProgramArguments'][7][5:])
        print('Launch Services may reuse existing Claude; a running process cannot be changed.')
    else:
        try:
            removed = uninstall(path)
        except (ValueError, RuntimeError, OSError) as error:
            parser.error(str(error))
        print('Login item removed; Claude was not quit.' if removed else 'Login item was not installed.')


if __name__ == '__main__':
    main()
