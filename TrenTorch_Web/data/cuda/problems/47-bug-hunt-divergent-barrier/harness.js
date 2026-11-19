const mk = (name, valid, seed, hidden) => { const X = H.rand(64, seed), e = []; for (let t = 0; t < 64; t++) e.push(63 - t < valid ? X[63 - t] : 0);
  return { name, hidden, buffers: [{type:'f32', data:X}, {type:'f32', data:H.zeros(64), read:true}],
    launches: [{ kernel: 'reverse_valid', grid: 1, block: 64, args: [{buf:0}, {buf:1}, valid] }], expect: {1: e} }; };
return { cases: [mk('valid = 64', 64, 1, false), mk('valid = 40', 40, 2, false), mk('valid = 17', 17, 3, true), mk('valid = 1', 1, 4, true)] };
