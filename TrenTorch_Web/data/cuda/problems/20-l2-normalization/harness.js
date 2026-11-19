const mk = (name, n, seed, hidden) => { const x = H.rand(n, seed, -3, 3); const d = Math.sqrt(x.reduce((a, v) => a + v * v, 0)); const blocks = Math.ceil(n / 256);
  return { name, hidden, tol: {abs: 1e-5, rel: 1e-3}, buffers: [{type:'f32', data:x}, {type:'f32', data:H.zeros(blocks)}, {type:'f32', data:[0]}, {type:'f32', data:H.zeros(n), read:true}],
    launches: [H.l1('sumsq_partials', n, [{buf:0}, {buf:1}, n], 256, 1024), { kernel: 'sum_final', grid: 1, block: 32, shared: 128, args: [{buf:1}, {buf:2}, blocks] }, H.l1('l2_map', n, [{buf:0}, {buf:3}, n, {buf:2}])],
    expect: {3: x.map((v) => v / d)} }; };
return { cases: [mk('N = 700', 700, 1, false), mk('N = 5000', 5000, 2, true), mk('N = 10', 10, 3, false)] };
