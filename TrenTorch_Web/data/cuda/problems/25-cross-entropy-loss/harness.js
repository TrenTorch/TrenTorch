const mk = (name, rows, K, seed, hidden, lo, hi) => { const Z = H.rand(rows * K, seed, lo, hi), T = H.ints(rows, seed + 1, 0, K - 1); const e = [];
  for (let r = 0; r < rows; r++) { const row = Z.slice(r * K, (r + 1) * K); const m = Math.max(...row); const s = row.reduce((a, v) => a + Math.exp(v - m), 0); e.push(m + Math.log(s) - row[T[r]]); }
  return { name, hidden, tol: {abs: 1e-3, rel: 1e-3}, buffers: [{type:'f32', data:Z}, {type:'i32', data:T}, {type:'f32', data:H.zeros(rows), read:true}],
    launches: [{ kernel: 'cross_entropy', grid: rows, block: 128, args: [{buf:0}, {buf:1}, {buf:2}, rows, K] }], expect: {2: e} }; };
return { cases: [mk('5 rows x 7 classes', 5, 7, 1, false, -3, 3), mk('4 rows x 300 classes', 4, 300, 2, false, -4, 4), mk('logits near 1000 (needs max subtraction)', 3, 50, 3, true, 995, 1005)] };
