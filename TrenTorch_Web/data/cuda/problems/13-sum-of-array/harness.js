const mk = (name, n, seed, hidden) => { const X = H.rand(n, seed, -1, 1); const blocks = Math.ceil(n / 256);
  return { name, hidden, tol: {abs:2e-3, rel:1e-3}, buffers: [{type:'f32', data:X}, {type:'f32', data:H.zeros(blocks)}, {type:'f32', data:[0], read:true}],
    launches: [H.l1('sum_partials', n, [{buf:0}, {buf:1}, n], 256, 256 * 4), { kernel: 'sum_final', grid: 1, block: 32, shared: 128, args: [{buf:1}, {buf:2}, blocks] }],
    expect: {2: [H.sum(X)]} }; };
return { cases: [mk('N = 1000', 1000, 1, false), mk('N = 8000 (31 blocks, final stage must handle many partials)', 8000, 2, true), mk('N = 7 (one partial block)', 7, 3, false)] };
