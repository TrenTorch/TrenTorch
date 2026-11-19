const lines = (t) => t.split('\n').filter((l) => /^rank \d+:/.test(l.trim())).map((l) => l.split(':')[1].trim().split(/\s+/).map(Number));
return { programs: [ { name: 'every rank holds all four shards in rank order', devices: 4, check: (r, text) => {
  const ls = lines(text); if (ls.length !== 4) return 'expected 4 lines "rank r: a b c d", found ' + ls.length;
  for (let k = 0; k < 4; k++) if ([1, 2, 3, 4].some((e, j) => Math.abs((ls[k][j] || 0) - e) > 1e-3)) return 'rank ' + k + ' printed [' + ls[k].join(', ') + '], expected [1, 2, 3, 4]';
  return null; } } ] };
