const mk = (name, n, seed, hidden, offset, spread) => { const X = H.rand(n, seed, offset - spread, offset + spread);
  let m = 0; for (const x of X) m += x; m /= n; let v = 0; for (const x of X) v += (x - m) * (x - m); v /= n;
  return { name, hidden, tol: {abs: 1e-3, rel: 2e-3}, buffers: [{type:'f32', data:X}, {type:'f32', data:[0, 0], read:true}],
    launches: [{ kernel: 'mean_var', grid: 1, block: 256, args: [{buf:0}, {buf:1}, n] }], expect: {1: [m, v]} }; };
return { cases: [mk('N = 1000, around 0', 1000, 1, false, 0, 3), mk('N = 3000, offset 10000, small spread', 3000, 2, false, 10000, 2), mk('N = 100 (fewer elements than threads)', 100, 3, true, 5, 1), mk('N = 4096, offset 50000', 4096, 4, true, 50000, 4)] };
