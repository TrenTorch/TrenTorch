const mk = (name, blocks, seed, hidden) => { const n = blocks * 128, X = H.rand(n, seed), e = new Array(n);
  for (let b = 0; b < blocks; b++) for (let t = 0; t < 128; t++) e[b * 128 + t] = X[b * 128 + 127 - t];
  return { name, hidden, buffers: [{type:'f32', data:X}, {type:'f32', data:H.zeros(n), read:true}],
    launches: [{ kernel: 'block_reverse', grid: blocks, block: 128, args: [{buf:0}, {buf:1}, n] }], expect: {1: e} }; };
return { cases: [mk('one block', 1, 1, false), mk('four blocks', 4, 2, false), mk('nine blocks', 9, 3, true)] };
