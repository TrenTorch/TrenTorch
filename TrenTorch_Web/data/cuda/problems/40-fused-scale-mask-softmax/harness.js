const mk = (name, rows, K, seed, hidden, scale, masked) => { const X = H.rand(rows * K, seed, -4, 4), M = H.ints(rows * K, seed + 1, 0, 3).map((v) => (v === 0 ? 0 : 1)); const e = [];
  masked.forEach((r) => { for (let j = 0; j < K; j++) M[r * K + j] = 0; });
  for (let r = 0; r < rows; r++) { const z = []; for (let j = 0; j < K; j++) if (M[r * K + j]) z.push(scale * X[r * K + j]); const m = Math.max(...z); const ex = z.map((v) => Math.exp(v - m)); const s = ex.reduce((a, b) => a + b, 0); let q = 0;
    for (let j = 0; j < K; j++) e.push(M[r * K + j] ? ex[q++] / s : 0); }
  return { name, hidden, tol: {abs: 1e-5, rel: 1e-3}, buffers: [{type:'f32', data:X}, {type:'i32', data:M}, {type:'f32', data:H.zeros(rows * K), read:true}],
    launches: [{ kernel: 'fused_scale_mask_softmax', grid: rows, block: 128, args: [{buf:0}, {buf:1}, {buf:2}, rows, K, scale] }], expect: {2: e} }; };
return { cases: [mk('3 rows x 12, scale 0.5', 3, 12, 1, false, 0.5, []), mk('4 rows x 200, scale 0.125', 4, 200, 2, false, 0.125, []), mk('a fully masked row gives zeros', 3, 40, 3, true, 1, [1]), mk('large scale 30', 2, 60, 4, true, 30, [])] };
