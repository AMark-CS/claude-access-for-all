"""Readable, privacy-conscious CLI reports."""
import os
import sys


def style(text, code):
    if sys.stdout.isatty() and not os.environ.get('NO_COLOR') and os.environ.get('TERM') != 'dumb':
        return f'\033[{code}m{text}\033[0m'
    return text


def title(name, subtitle):
    return [
        '',
        '  ' + style('CLAUDE ACCESS', '1;36') + style('  /  ' + name.upper(), '1'),
        '  ' + style(subtitle, '2'),
        '',
    ]


def row(label, value):
    return f'  {label:<20} {value}'


def section(name):
    return '\n  ' + style(name, '1')


def group(label, names, values):
    active = [name for name in names if values.get(name)]
    if active:
        return row(label, style('Set', '33') + '  ' + ', '.join(active))
    return row(label, style('Not set', '2'))


def render_doctor(report):
    env = report['environment_set']
    system = report['system']
    if system == 'Darwin':
        system = 'macOS ' + (report['macos_version'] or '(version unavailable)')
    lines = title('Environment check', 'Local diagnostic · no network requests')
    lines += [
        row('System', system + '  ·  ' + report['architecture']),
        row('Claude Code', style('Found on PATH', '32') if report['claude_on_path'] else style('Not found on PATH', '33')),
        section('Environment variables'),
        group('Authentication', ('ANTHROPIC_API_KEY', 'ANTHROPIC_AUTH_TOKEN'), env),
        group('Service endpoint', ('ANTHROPIC_BASE_URL',), env),
        group('Cloud providers', ('CLAUDE_CODE_USE_BEDROCK', 'CLAUDE_CODE_USE_VERTEX', 'CLAUDE_CODE_USE_FOUNDRY'), env),
        group('Proxy variables', ('HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'NO_PROXY', 'http_proxy', 'https_proxy', 'all_proxy', 'no_proxy'), env),
        group('TLS settings', ('NODE_EXTRA_CA_CERTS', 'NODE_TLS_REJECT_UNAUTHORIZED'), env),
        '',
    ]
    if report['warnings']:
        lines.append('  ' + style('Things to review', '1;33'))
        lines.extend('  • ' + warning for warning in report['warnings'])
    else:
        lines.append('  ' + style('No local configuration warnings.', '32'))
    lines += ['', '  Values are never shown. System proxies, app settings, credentials,',
              '  billing, account eligibility and network access were not checked.', '']
    return '\n'.join(lines)


def render_audit(report):
    names = list(dict.fromkeys(name for name in report['process_timezone_names'] if name))
    tz = ' / '.join(names) if names else 'Unavailable'
    lines = title('CLI signal audit', 'Current terminal process · offline')
    lines += [
        row('System', report['system']),
        row('Claude Code', style('Found on PATH', '32') if report['claude_on_path'] else style('Not found on PATH', '33')),
        section('Locale & time'),
        row('Timezone names', tz),
        row('TZ override', style('Set', '33') if report['timezone_override_set'] else style('Not set', '2')),
        group('Locale variables', ('LANG', 'LC_ALL', 'LC_TIME'), report['locale_overrides_set']),
        section('Connection & authentication'),
        group('Endpoint & proxies', report['routing_overrides_set'].keys(), report['routing_overrides_set']),
        group('Credentials', report['credential_overrides_set'].keys(), report['credential_overrides_set']),
        '',
        '  Values are never shown. HKT and other abbreviations are timezone names,',
        '  not proof of an exact location. Browser, Desktop, network, IP and',
        '  account status were not checked.',
        '',
        '  Next: run ' + style('claude-access inspect', '1') + ' to inspect your default browser.',
        '',
    ]
    return '\n'.join(lines)
