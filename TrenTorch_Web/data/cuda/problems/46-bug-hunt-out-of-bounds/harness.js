const mk = (name, n, seed, hidden) => { const X = H.rand(n, seed);
  return { name, hidden, buffers: [{type:'f32', data:X}, {type:'f32', data:H.zeros(n), read:true}],
    launches: [H.l1('double_it', n, [{buf:0}, {buf:1}, n])], expect: {1: X.map((v) => 2 * v)} }; };
return { cases: [mk('N = 1000', 1000, 1, false), mk('N = 4099', 4099, 2, false), mk('N = 5001', 5001, 3, true)] };
