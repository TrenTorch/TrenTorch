const sm = (row) => { const m = Math.max(...row); const e = row.map((v) => Math.exp(v - m)); const s = e.reduce((a, b) => a + b, 0); return e.map((v) => v / s); };
const mk = (name, rows, K, seed, hidden, lo, hi) => { const X = H.rand(rows * K, seed, lo, hi); let e = [];
  for (let r = 0; r < rows; r++) e = e.concat(sm(X.slice(r * K, (r + 1) * K)));
  return { name, hidden, tol: {abs: 1e-5, rel: 1e-3}, buffers: [{type:'f32', data:X}, {type:'f32', data:H.zeros(rows * K), read:true}],
    launches: [{ kernel: 'softmax_rows', grid: rows, block: 128, args: [{buf:0}, {buf:1}, rows, K] }], expect: {1: e} }; };
return { cases: [mk('4 rows x 10', 4, 10, 1, false, -3, 3), mk('3 rows x 300 (wider than the block)', 3, 300, 2, false, -4, 4), mk('large logits around 1000 (needs max subtraction)', 2, 150, 3, true, 995, 1005), mk('1 row x 1', 1, 1, 4, true, -2, 2)] };
