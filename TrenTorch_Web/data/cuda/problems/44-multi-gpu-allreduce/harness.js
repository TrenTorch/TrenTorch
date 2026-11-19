const lines = (t) => t.split('\n').filter((l) => /^rank \d+:/.test(l.trim()));
return { devices: 4, programs: [
  { name: 'all four ranks hold the sum 15', devices: 4, check: (r, text) => {
      const ls = lines(text);
      if (ls.length !== 4) return 'expected 4 lines "rank r: value", found ' + ls.length;
      const bad = ls.find((l) => Math.abs(parseFloat(l.split(':')[1]) - 15) > 1e-3);
      return bad ? 'wrong value: "' + bad.trim() + '", expected 15.000000' : (r.counters.ncclOps > 0 ? null : 'no NCCL collective was recorded');
  } }
] };
