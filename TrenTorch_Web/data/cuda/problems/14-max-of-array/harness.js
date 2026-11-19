const mk = (name, n, seed, hidden) => { const X = H.rand(n, seed, -9, -1); const blocks = Math.ceil(n / 256);
  return { name, hidden, tol: {abs:1e-6, rel:1e-6}, buffers: [{type:'f32', data:X}, {type:'f32', data:H.zeros(blocks)}, {type:'f32', data:[0], read:true}],
    launches: [H.l1('max_partials', n, [{buf:0}, {buf:1}, n], 256, 256 * 4), { kernel: 'max_final', grid: 1, block: 32, shared: 128, args: [{buf:1}, {buf:2}, blocks] }],
    expect: {2: [Math.max(...X)]} }; };
return { cases: [mk('N = 1000, all negative', 1000, 1, false), mk('N = 8000, all negative', 8000, 2, true), mk('N = 7', 7, 3, false)] };
