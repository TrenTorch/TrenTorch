const mk = (name, D, h, w, KD, KH, KW, seed, hidden) => { const X = H.rand(D * h * w, seed), F = H.rand(KD * KH * KW, seed + 1), e = [];
  for (let z = 0; z < D; z++) for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { let a = 0;
    for (let kz = 0; kz < KD; kz++) for (let ky = 0; ky < KH; ky++) for (let kx = 0; kx < KW; kx++) { const iz = z + kz - (KD >> 1), iy = y + ky - (KH >> 1), ix = x + kx - (KW >> 1);
      if (ix >= 0 && ix < w && iy >= 0 && iy < h && iz >= 0 && iz < D) a += X[(iz * h + iy) * w + ix] * F[(kz * KH + ky) * KW + kx]; } e.push(a); }
  return { name, hidden, tol: {abs: 1e-5, rel: 1e-3}, buffers: [{type:'f32', data:X}, {type:'f32', data:F}, {type:'f32', data:H.zeros(D * h * w), read:true}],
    launches: [H.l3('conv3d', w, h, D, [{buf:0}, {buf:1}, {buf:2}, D, h, w, KD, KH, KW])], expect: {2: e} }; };
return { cases: [mk('3 x 4 x 5, 3 x 3 x 3', 3, 4, 5, 3, 3, 3, 1, false), mk('5 x 6 x 9, 3 x 3 x 3 (crosses blocks)', 5, 6, 9, 3, 3, 3, 2, false), mk('4 x 5 x 6, 1 x 3 x 5', 4, 5, 6, 1, 3, 5, 3, true)] };
