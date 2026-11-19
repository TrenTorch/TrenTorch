const mk = (name, n, seed, hidden) => { const A = H.rand(n, seed), B = H.rand(n, seed + 1); let e = 0; for (let i = 0; i < n; i++) e += A[i] * B[i];
  return { name, hidden, tol: {abs: 3e-3, rel: 1e-3}, buffers: [{type:'f32', data:A}, {type:'f32', data:B}, {type:'f32', data:H.zeros(8)}, {type:'f32', data:[0], read:true}],
    launches: [{ kernel: 'dot_partials', grid: 8, block: 256, shared: 1024, args: [{buf:0}, {buf:1}, {buf:2}, n] }, { kernel: 'dot_final', grid: 1, block: 32, shared: 128, args: [{buf:2}, {buf:3}, 8] }], expect: {3: [e]} }; };
return { cases: [mk('N = 1000', 1000, 1, false), mk('N = 5000 (several elements per thread)', 5000, 2, false), mk('N = 9 (most threads idle)', 9, 3, true)] };
