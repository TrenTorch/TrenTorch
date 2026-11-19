const mk = (name, T, D, seed, hidden, mag) => { const Q = H.rand(T * D, seed, -mag, mag), Km = H.rand(T * D, seed + 1, -mag, mag), V = H.rand(T * D, seed + 2, -1, 1), e = [];
  for (let r = 0; r < T; r++) { const sc = []; for (let j = 0; j < T; j++) { let d = 0; for (let k = 0; k < D; k++) d += Q[r * D + k] * Km[j * D + k]; sc.push(d / Math.sqrt(D)); }
    const m = Math.max(...sc); const ex = sc.map((v) => Math.exp(v - m)); const s = ex.reduce((a, b) => a + b, 0);
    for (let k = 0; k < D; k++) { let a = 0; for (let j = 0; j < T; j++) a += (ex[j] / s) * V[j * D + k]; e.push(a); } }
  return { name, hidden, tol: {abs: 2e-4, rel: 2e-3}, buffers: [{type:'f32', data:Q}, {type:'f32', data:Km}, {type:'f32', data:V}, {type:'f32', data:H.zeros(T * D), read:true}],
    launches: [{ kernel: 'attention', grid: T, block: 64, args: [{buf:0}, {buf:1}, {buf:2}, {buf:3}, T, D] }], expect: {3: e} }; };
return { cases: [mk('T = 4, D = 4', 4, 4, 1, false, 1), mk('T = 20, D = 16', 20, 16, 2, false, 1), mk('T = 33, D = 8, large scores', 33, 8, 3, true, 8), mk('T = 64, D = 64', 64, 64, 4, true, 1)] };
