const mk = (name, rows, K, seed, hidden) => { const X = H.rand(rows * K, seed, -3, 3), W = H.rand(K, seed + 1, 0.5, 1.5), eps = 1e-5; const e = [];
  for (let r = 0; r < rows; r++) { let ms = 0; for (let j = 0; j < K; j++) ms += X[r * K + j] ** 2; const inv = 1 / Math.sqrt(ms / K + eps); for (let j = 0; j < K; j++) e.push(X[r * K + j] * inv * W[j]); }
  return { name, hidden, tol: {abs: 1e-5, rel: 1e-3}, buffers: [{type:'f32', data:X}, {type:'f32', data:W}, {type:'f32', data:H.zeros(rows * K), read:true}],
    launches: [{ kernel: 'rms_norm', grid: rows, block: 128, args: [{buf:0}, {buf:1}, {buf:2}, rows, K, eps] }], expect: {2: e} }; };
return { cases: [mk('4 rows x 16', 4, 16, 1, false), mk('3 rows x 300', 3, 300, 2, false), mk('5 rows x 129', 5, 129, 3, true)] };
