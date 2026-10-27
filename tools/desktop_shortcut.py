#!/usr/bin/env python3
"""Create a standalone macOS app that requests the Claude Access environment."""
import argparse
from pathlib import Path
import plistlib
import shlex
import sys

from privacy import validate_locale, validate_timezone


def create_bundle(destination, timezone, locale):
    """Create a new app bundle, refusing to overwrite an existing path."""
    destination = Path(destination).expanduser().absolute()
    destination.mkdir(parents=False, exist_ok=False)
    try:
        contents = destination / 'Contents'
        macos = contents / 'MacOS'
        macos.mkdir(parents=True)
        info = {
            'CFBundleIdentifier': 'org.claudeaccess.launcher',
            'CFBundleName': 'Claude Access Launcher',
            'CFBundleDisplayName': 'Claude Access Launcher',
            'CFBundleExecutable': 'launch-claude',
            'CFBundlePackageType': 'APPL',
            'CFBundleShortVersionString': '1.0',
            'LSMinimumSystemVersion': '13.0',
            'LSUIElement': True,
        }
        (contents / 'Info.plist').write_bytes(plistlib.dumps(info))
        args = ['/usr/bin/open', '-n', '-a', 'Claude',
                '--env', 'TZ=' + timezone, '--env', 'LANG=' + locale,
                '--env', 'LC_ALL=' + locale]
        script = '#!/bin/sh\n# Launch Claude with explicitly scoped environment requests.\nexec ' + ' '.join(shlex.quote(arg) for arg in args) + '\n'
        executable = macos / 'launch-claude'
        executable.write_text(script, encoding='utf-8')
        executable.chmod(0o755)
    except BaseException:
        # Only remove files created by this call; no pre-existing target is touched.
        import shutil
        shutil.rmtree(destination)
        raise
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('Claude Access Launcher.app'),
                        help='New .app path; parent must exist. Defaults to the current directory.')
    parser.add_argument('--timezone', type=validate_timezone, default='America/Los_Angeles')
    parser.add_argument('--locale', type=validate_locale, default='en_US.UTF-8')
    args = parser.parse_args()
    if sys.platform != 'darwin':
        parser.error('The launcher requires macOS.')
    if args.output.suffix != '.app':
        parser.error('Output must end in .app.')
    try:
        bundle = create_bundle(args.output, args.timezone, args.locale)
    except FileExistsError:
        parser.error(f'Target already exists: {args.output}. Choose a different --output path.')
    except OSError as error:
        parser.error(str(error))
    print(f'Created: {bundle}')
    print('Quit Claude first, then open the launcher. You can drag it to the Dock.')
    print('Switch to the launched Claude app with Command-Tab.')
    print('Launch Services requests process settings; Claude may use existing services or system settings.')


if __name__ == '__main__':
    main()
