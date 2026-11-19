const mk = (name, n, seed, hidden) => { const X = H.rand(n, seed, -3, 3);
  return { name, hidden, buffers: [{type:'f32', data:X}, {type:'f32', data:H.zeros(n), read:true}],
    launches: [H.l1('relu_float4', Math.floor(n / 4) + 3, [{buf:0}, {buf:1}, n], 128)], expect: {1: X.map((x) => Math.max(x, 0))},
    check: (o, c) => (n >= 64 && c.globalLoadBytes / Math.max(1, c.globalLoads) < 8 ? 'every load moved about ' + (c.globalLoadBytes / c.globalLoads).toFixed(1) + ' bytes; use float4 so a load moves 16' : null) }; };
return { cases: [mk('N = 1000 (divisible by 4)', 1000, 1, false), mk('N = 1003 (tail of 3)', 1003, 2, false), mk('N = 3 (only a tail)', 3, 3, true), mk('N = 4097', 4097, 4, true)] };
