const mk = (name, n, bins, seed, hidden, skew) => { const raw = H.ints(n, seed, 0, bins - 1); const x = skew ? raw.map((v, i) => (i % 3 ? 0 : v)) : raw;
  x[3] = bins; x[5] = -1;   // out-of-range keys must be ignored
  const e = H.zeros(bins); x.forEach((v) => { if (v >= 0 && v < bins) e[v]++; });
  return { name, hidden, buffers: [{type:'i32', data:x}, {type:'i32', data:H.zeros(bins), read:true}],
    launches: [H.l1('histogram', n, [{buf:0}, {buf:1}, n, bins])], expect: {1: e} }; };
return { cases: [mk('n = 100, 8 bins', 100, 8, 1, false, false), mk('n = 1000, 16 bins', 1000, 16, 2, false, false), mk('n = 3000, 64 bins, heavily skewed', 3000, 64, 3, true, true)] };
