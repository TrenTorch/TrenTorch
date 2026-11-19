const mk = (name, n, seed, hidden) => { const A = H.rand(n, seed, -2, 2), B = H.rand(n, seed + 9, -2, 2); let d = 0, aa = 0, bb = 0;
  for (let i = 0; i < n; i++) { d += A[i] * B[i]; aa += A[i] * A[i]; bb += B[i] * B[i]; }
  return { name, hidden, tol: {abs: 2e-4, rel: 1e-3}, buffers: [{type:'f32', data:A}, {type:'f32', data:B}, {type:'f32', data:H.zeros(24)}, {type:'f32', data:[0], read:true}],
    launches: [{ kernel: 'cos_partials', grid: 8, block: 256, shared: 3072, args: [{buf:0}, {buf:1}, {buf:2}, n] }, { kernel: 'cos_final', grid: 1, block: 32, shared: 384, args: [{buf:2}, {buf:3}, 8] }], expect: {3: [d / (Math.sqrt(aa) * Math.sqrt(bb))]} }; };
return { cases: [mk('N = 1000', 1000, 1, false), mk('N = 4000', 4000, 2, true), mk('N = 13', 13, 3, false)] };
