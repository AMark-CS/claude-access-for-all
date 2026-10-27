'use strict';

// This local page intentionally performs no fetch, analytics, STUN, or storage.
function signals() {
  const intl = Intl.DateTimeFormat().resolvedOptions();
  const fonts = ['PingFang SC', 'Microsoft YaHei', 'MiSans', 'HarmonyOS Sans', 'OPPO Sans'];
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  const sample = '汉字测试ABCwW0123';
  const bases = ['monospace', 'serif', 'sans-serif'];
  const measure = font => { ctx.font = `32px ${font}`; return ctx.measureText(sample).width; };
  const available = ctx ? fonts.filter(name => bases.some(base =>
    measure(`"${name}",${base}`) !== measure(base))) : [];
  return [
    ['Time zone', intl.timeZone || 'Unavailable'],
    ['UTC offset', String(-new Date().getTimezoneOffset() / 60) + ' hours'],
    ['Browser languages', (navigator.languages || [navigator.language]).join(', ') || 'Unavailable'],
    ['Intl locale', intl.locale || 'Unavailable'],
    ['User agent', navigator.userAgent || 'Unavailable'],
    ['Platform', navigator.platform || 'Unavailable'],
    ['Font width probes', ctx ? (available.join(', ') || 'No listed font distinguished from fallbacks') : 'Unavailable'],
  ];
}

document.getElementById('scan').addEventListener('click', () => {
  const list = document.getElementById('signals');
  list.replaceChildren();
  try {
    for (const [name, value] of signals()) {
      const term = document.createElement('dt');
      const description = document.createElement('dd');
      term.textContent = name;
      description.textContent = value;
      list.append(term, description);
    }
    document.getElementById('results').hidden = false;
    document.getElementById('status').textContent = 'Inspection complete. Results are local to this page.';
  } catch (error) {
    document.getElementById('status').textContent = 'Inspection failed in this browser.';
  }
});
