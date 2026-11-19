const lines = (t) => t.split('\n').filter((l) => /^rank \d+:/.test(l.trim())).map((l) => l.split(':')[1].trim().split(/\s+/).map(Number));
return { programs: [ { name: 'each rank keeps its shard of the sum', devices: 4, check: (r, text) => {
  const ls = lines(text); if (ls.length !== 4) return 'expected 4 lines "rank r: a b", found ' + ls.length;
  for (let k = 0; k < 4; k++) { const e = [10 * (2 * k + 1), 10 * (2 * k + 2)]; if (e.some((v, j) => Math.abs((ls[k][j] || 0) - v) > 1e-3)) return 'rank ' + k + ' printed [' + ls[k].join(', ') + '], expected [' + e.join(', ') + ']'; }
  return null; } } ] };
