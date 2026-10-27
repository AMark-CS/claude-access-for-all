import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const cli = join(root, 'bin/claude-access.js');
const run = (...args) => spawnSync(process.execPath, [cli, ...args], { encoding: 'utf8' });

test('help and unknown commands have useful exit codes', () => {
  assert.match(run('--help').stdout, /interactive menu/);
  assert.equal(run('--help').status, 0);
  assert.equal(run('bogus').status, 2);
});

test('audit reaches packaged Python without exposing secrets', () => {
  const marker = 'test-secret-not-for-output';
  const result = spawnSync(process.execPath, [cli, 'audit'], { encoding: 'utf8', env: { ...process.env, ANTHROPIC_API_KEY: marker } });
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /ANTHROPIC_API_KEY/);
  assert.ok(!result.stdout.includes(marker));
});

test('reminder output is a calendar and invalid dates fail', () => {
  const good = run('reminder', '--renewal', '2099-12-01');
  assert.equal(good.status, 0, good.stderr);
  assert.match(good.stdout, /BEGIN:VCALENDAR/);
  assert.equal(run('reminder', '--renewal', 'invalid').status, 2);
});

test('menu handles noninteractive sessions without hanging', () => {
  const result = run('menu');
  assert.equal(result.status, 1);
  assert.match(result.stderr, /needs a terminal/);
});


test('default diagnostics are readable and identify active variables without values', () => {
  const marker = 'test-secret-never-for-display';
  for (const command of ['doctor', 'audit']) {
    const result = spawnSync(process.execPath, [cli, command], { encoding: 'utf8', env: { ...process.env, ANTHROPIC_API_KEY: marker, NO_COLOR: '1' } });
    assert.equal(result.status, 0, result.stderr);
    assert.match(result.stdout, /CLAUDE ACCESS/);
    assert.match(result.stdout, /ANTHROPIC_API_KEY/);
    assert.ok(!result.stdout.includes(marker));
    assert.ok(!result.stdout.includes('\u001b['));
    assert.throws(() => JSON.parse(result.stdout));
  }
});

test('score shows a partial denominator and disabled JSON option', () => {
  const result = run('score');
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /Partial score/);
  assert.match(result.stdout, /Not measured/);
  assert.equal(run('doctor', '--json').status, 2);
  assert.equal(run('audit', '--json').status, 2);
  assert.equal(run('score', '--json').status, 2);
});
