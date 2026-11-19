const lines = (t) => t.split('\n').filter((l) => /^rank \d+:/.test(l.trim())).map((l) => l.split(':')[1].trim().split(/\s+/).map(Number));
return { programs: [ { name: 'every rank receives the root data', devices: 4, check: (r, text) => {
  const ls = lines(text); if (ls.length !== 4) return 'expected 4 lines "rank r: value", found ' + ls.length;
  const bad = ls.findIndex((v) => Math.abs(v[0] - 7.5) > 1e-3); return bad >= 0 ? 'rank ' + bad + ' printed ' + ls[bad][0] + ', expected 7.5' : null; } } ] };
