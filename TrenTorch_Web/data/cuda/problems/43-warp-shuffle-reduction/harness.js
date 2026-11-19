const mk = (name, n, seed, hidden) => { const X = H.ints(n, seed, 0, 20), blocks = Math.ceil(n / 32), e = [];
  for (let b = 0; b < blocks; b++) { let s = 0; for (let j = 0; j < 32; j++) if (b * 32 + j < n) s += X[b * 32 + j]; e.push(s); }
  return { name, hidden, buffers: [{type:'f32', data:X}, {type:'f32', data:H.zeros(blocks), read:true}],
    launches: [{ kernel: 'warp_sum_kernel', grid: blocks, block: 32, args: [{buf:0}, {buf:1}, n] }], expect: {1: e},
    check: (o, c) => (c.sharedLoads + c.sharedStores > 0 ? 'correct, but it used shared memory (' + (c.sharedLoads + c.sharedStores) + ' accesses): do the exchange with warp shuffles instead' : null) }; };
return { cases: [mk('N = 32 (one full warp)', 32, 1, false), mk('N = 1000 (partial last warp)', 1000, 2, false), mk('N = 5', 5, 3, true), mk('N = 4096', 4096, 4, true)] };
