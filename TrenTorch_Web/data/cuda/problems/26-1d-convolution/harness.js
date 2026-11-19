const mk = (name, N, R, seed, hidden) => { const x = H.rand(N, seed), w = H.rand(2 * R + 1, seed + 1), e = [];
  for (let i = 0; i < N; i++) { let a = 0; for (let k = -R; k <= R; k++) { const j = i + k; if (j >= 0 && j < N) a += x[j] * w[k + R]; } e.push(a); }
  return { name, hidden, tol: {abs: 1e-5, rel: 1e-3}, buffers: [{type:'f32', data:x}, {type:'f32', data:w}, {type:'f32', data:H.zeros(N), read:true}],
    launches: [H.l1('conv1d', N, [{buf:0}, {buf:1}, {buf:2}, N, R])], expect: {2: e} }; };
return { cases: [mk('N = 20, R = 1', 20, 1, 1, false), mk('N = 1000, R = 3 (crosses block boundaries)', 1000, 3, 2, false), mk('N = 600, R = 7', 600, 7, 3, true), mk('N = 5, R = 9 (filter wider than input)', 5, 9, 4, true)] };
