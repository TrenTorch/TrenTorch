const lines = (t) => t.split('\n').filter((l) => /^rank \d+:/.test(l.trim()));
return { programs: [
  { name: 'both ranks issue the same collectives in the same order', devices: 2, check: (r, text) => {
      const ls = lines(text);
      if (ls.length !== 2) return 'expected 2 lines "rank r: value", found ' + ls.length;
      const bad = ls.find((l) => Math.abs(parseFloat(l.split(':')[1]) - 3) > 1e-3);
      return bad ? 'wrong value: "' + bad.trim() + '", expected 3.000000' : null;
  } }
] };
