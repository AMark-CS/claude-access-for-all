#!/usr/bin/env node
import { spawnSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { createInterface } from 'node:readline/promises';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const help = `Claude Access for All

Usage: claude-access [command] [options]

  menu                   Open the interactive menu (default)
  doctor                 Check local installation and configuration presence
  audit                  Inspect CLI environment signals locally
  score                  Score locally observable timezone signals
  cli [options] [-- ...] Launch Claude Code with scoped locale settings
  app [options]          Launch Claude Desktop with scoped locale settings
  desktop-shortcut       Create a standalone macOS launcher app
  web [options]          Launch Claude in a separate browser profile
  inspect                Open the local browser signal inspector
  reminder [options]     Write a one-time calendar event to stdout
  guide                  Open the English privacy and access guide
  help                   Show this help
  version                Show the package version

Examples:
  claude-access cli --timezone America/Los_Angeles -- --version
  claude-access web --browser edge --timezone America/Los_Angeles
  claude-access reminder --renewal 2026-12-01 --days-before 3 > renewal.ics

Requires macOS, Node.js 18+, and Python 3.9+. Launching Claude requires the
relevant installed app and a valid account. Local signal checks are not a ban
prediction or an eligibility test. For options run a command with --help.`;

function run(command, args) {
  const result = spawnSync(command, args, { stdio: 'inherit' });
  if (result.error) {
    const hint = result.error.code === 'ENOENT' && command === 'python3'
      ? 'Python 3.9+ is required. Install Python from https://www.python.org/downloads/macos/.'
      : `Could not start ${command}: ${result.error.message}`;
    console.error(hint);
    return 1;
  }
  return result.status ?? 1;
}

function dispatch(command, args = []) {
  switch (command) {
    case 'doctor': return run('python3', [join(root, 'tools/access.py'), 'doctor', ...args]);
    case 'audit': return run('python3', [join(root, 'tools/privacy.py'), 'audit', ...args]);
    case 'score': return run('python3', [join(root, 'tools/score.py'), ...args]);
    case 'desktop-shortcut': return run('python3', [join(root, 'tools/desktop_shortcut.py'), ...args]);
    case 'cli': case 'app': case 'web':
      return run('python3', [join(root, 'tools/privacy.py'), command, ...args]);
    case 'reminder': return run('python3', [join(root, 'tools/access.py'), 'reminder', ...args]);
    case 'inspect':
      if (process.platform !== 'darwin') { console.error('The inspector launcher requires macOS.'); return 1; }
      return run('/usr/bin/open', [join(root, 'web/fingerprint.html')]);
    case 'guide':
      if (process.platform !== 'darwin') { console.error('The guide launcher requires macOS.'); return 1; }
      return run('/usr/bin/open', ['https://github.com/AMark-CS/claude-access-for-all/blob/main/docs/privacy-inspector.md']);
    case 'help': case '--help': case '-h': console.log(help); return 0;
    case 'version': case '--version': case '-v': console.log(JSON.parse(readFileSync(join(root, 'package.json'), 'utf8')).version); return 0;
    default: console.error(`Unknown command: ${command}\n\n${help}`); return 2;
  }
}

async function menu() {
  if (!process.stdin.isTTY || !process.stdout.isTTY) {
    console.error('The interactive menu needs a terminal. Use claude-access help for commands.');
    return 1;
  }
  const rl = createInterface({ input: process.stdin, output: process.stdout });
  try {
    console.log(`\nClaude Access for All\n\n  1  Check local environment\n  2  Inspect CLI signals\n  3  Start Claude Code\n  4  Start Claude Desktop\n  5  Start Claude in a separate browser profile\n  6  Open browser signal inspector\n  7  Open the privacy guide\n  8  Create a renewal calendar file\n  9  Score local timezone signals\n  10 Create a macOS desktop launcher\n  0  Exit\n`);
    const choice = (await rl.question('Choose an option: ')).trim();
    if (choice === '0') return 0;
    const simple = { '1': 'doctor', '2': 'audit', '3': 'cli', '4': 'app', '6': 'inspect', '7': 'guide', '9': 'score', '10': 'desktop-shortcut' };
    if (simple[choice]) { rl.close(); return dispatch(simple[choice]); }
    if (choice === '5') {
      const browser = (await rl.question('Browser (chrome/edge) [chrome]: ')).trim() || 'chrome';
      if (!['chrome', 'edge'].includes(browser)) { console.error('Choose chrome or edge.'); return 2; }
      rl.close(); return dispatch('web', ['--browser', browser]);
    }
    if (choice === '8') {
      const renewal = (await rl.question('Next renewal date (YYYY-MM-DD): ')).trim();
      const output = (await rl.question('Output file path [renewal.ics]: ')).trim() || 'renewal.ics';
      const lead = (await rl.question('Days before renewal [3]: ')).trim() || '3';
      rl.close();
      const result = spawnSync('python3', [join(root, 'tools/access.py'), 'reminder', '--renewal', renewal, '--days-before', lead], { encoding: 'utf8' });
      if (result.error) { console.error('Could not start Python 3.9+.'); return 1; }
      if (result.status !== 0) { console.error(result.stderr.trim()); return result.status ?? 1; }
      const { writeFileSync } = await import('node:fs');
      try { writeFileSync(output, result.stdout, { flag: 'wx', mode: 0o600 }); }
      catch (error) { console.error(`Could not create calendar file: ${error.message}`); return 1; }
      console.log(`Created ${output}. Import it into Calendar and check notification settings.`);
      return 0;
    }
    console.error('Unknown option. Run the menu again to choose 0–10.');
    return 2;
  } finally { rl.close(); }
}

const [command = 'menu', ...args] = process.argv.slice(2);
process.exitCode = command === 'menu' ? await menu() : dispatch(command, args);
