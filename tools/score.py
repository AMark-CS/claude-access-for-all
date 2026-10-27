"""Local partial signal score, adapted from LinXiaoTao/FuckClaude (MIT)."""
import argparse
import datetime
import os
from pathlib import Path

from report import section, style, title

# Based on src/config/signals.ts in LinXiaoTao/FuckClaude, master as reviewed
# 2026-10-27. Browser-only measurements are deliberately not substituted.
MAINLAND_ZONES = frozenset(('Asia/Shanghai', 'Asia/Urumqi', 'Asia/Chongqing',
                            'Asia/Chungking', 'Asia/Harbin', 'Asia/Kashgar'))
OTHER_ZONES = frozenset(('Asia/Hong_Kong', 'Asia/Macau'))


def timezone_name(env=None, localtime='/etc/localtime'):
    env = os.environ if env is None else env
    if 'TZ' in env:
        # POSIX strings and empty values are not necessarily IANA timezones.
        value = env['TZ'].lstrip(':')
        if value == 'UTC':
            return value
        parts = value.split('/')
        if len(parts) > 1 and all(part and part not in ('.', '..') for part in parts):
            if (Path('/usr/share/zoneinfo') / value).is_file():
                return value
        return None
    try:
        target = str(Path(localtime).resolve(strict=True))
    except (OSError, RuntimeError):
        return None
    marker = '/zoneinfo/'
    return target.split(marker, 1)[1] if marker in target else None


def timezone_weight(name):
    if name is None:
        return None
    if name in MAINLAND_ZONES:
        return 1.0
    if name in OTHER_ZONES:
        return 0.6
    return 0.0


def collect():
    name = timezone_name()
    offset = datetime.datetime.now().astimezone().utcoffset()
    minutes = int(offset.total_seconds() / 60) if offset is not None else None
    return {'timezone': name, 'offset_minutes': minutes}


def render_score(data):
    name = data['timezone']
    ratio = timezone_weight(name)
    minutes = data['offset_minutes']
    tz_points = None if ratio is None else ratio * 24
    offset_points = None if minutes is None else (2.1 if minutes == 480 else 0)
    values = [x for x in (tz_points, offset_points) if x is not None]
    possible = (24 if tz_points is not None else 0) + (3 if offset_points is not None else 0)
    points = sum(values)
    bar_filled = round(points / possible * 24) if possible else 0
    bar = '█' * bar_filled + '░' * (24 - bar_filled)
    lines = title('Local signal score', 'Terminal-only snapshot · offline')
    if possible:
        lines += ['  ' + style(f'{points:g} / {possible} points', '1;36'),
                  '  ' + style(bar, '36'),
                  '  Partial score · available signals only · not a 100-point result', '']
    else:
        lines += ['  Score unavailable · no supported signals could be read', '']
    lines += [section('Measured signals')]
    lines += [f"  {'Timezone':<16} {(name or 'Unavailable'):<28} " +
              (f'{tz_points:g} / 24' if tz_points is not None else 'not scored')]
    if minutes is None:
        offset_text = 'Unavailable'
    else:
        hours, mins = divmod(abs(minutes), 60)
        offset_text = f"UTC{'+' if minutes >= 0 else '-'}{hours:02d}:{mins:02d}"
    lines += [f"  {'UTC offset':<16} {offset_text:<28} " +
              (f'{offset_points:g} / 3' if offset_points is not None else 'not scored')]
    lines += [section('Not measured'),
              '  Browser language & Intl locale     Browser fonts & vendor fonts',
              '  Browser / device identity          WebRTC & emoji rendering',
              '',
              '  This is a third-party heuristic, not an Anthropic risk score or',
              '  ban prediction. It cannot assess IP, billing or account status.',
              '  Browser signals need a browser; run claude-access inspect.',
              '  To inspect the launcher timezone, run:',
              '  TZ=America/Los_Angeles claude-access score', '']
    return '\n'.join(lines)


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    print(render_score(collect()))


if __name__ == '__main__':
    main()
