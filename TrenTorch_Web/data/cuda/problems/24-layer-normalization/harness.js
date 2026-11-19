const mk = (name, rows, K, seed, hidden, off) => { const X = H.rand(rows * K, seed, off - 2, off + 2), g = H.rand(K, seed + 1, 0.5, 1.5), b = H.rand(K, seed + 2, -1, 1), eps = 1e-5; const e = [];
  for (let r = 0; r < rows; r++) { let m = 0; for (let j = 0; j < K; j++) m += X[r * K + j]; m /= K; let v = 0; for (let j = 0; j < K; j++) v += (X[r * K + j] - m) ** 2; v /= K; const inv = 1 / Math.sqrt(v + eps);
    for (let j = 0; j < K; j++) e.push((X[r * K + j] - m) * inv * g[j] + b[j]); }
  return { name, hidden, tol: {abs: 2e-4, rel: 1e-3}, buffers: [{type:'f32', data:X}, {type:'f32', data:g}, {type:'f32', data:b}, {type:'f32', data:H.zeros(rows * K), read:true}],
    launches: [{ kernel: 'layer_norm', grid: rows, block: 128, args: [{buf:0}, {buf:1}, {buf:2}, {buf:3}, rows, K, eps] }], expect: {3: e} }; };
return { cases: [mk('4 rows x 16', 4, 16, 1, false, 0), mk('3 rows x 300', 3, 300, 2, false, 1), mk('offset 1000 (cancellation)', 3, 200, 3, true, 1000), mk('2 rows x 129', 2, 129, 4, true, 5)] };
