const mk = (name, h, w, fh, fw, seed, hidden) => { const X = H.rand(h * w, seed), F = H.rand(fh * fw, seed + 1), e = [];
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { let a = 0; for (let ky = 0; ky < fh; ky++) for (let kx = 0; kx < fw; kx++) { const iy = y + ky - (fh >> 1), ix = x + kx - (fw >> 1); if (ix >= 0 && ix < w && iy >= 0 && iy < h) a += X[iy * w + ix] * F[ky * fw + kx]; } e.push(a); }
  return { name, hidden, tol: {abs: 1e-5, rel: 1e-3}, buffers: [{type:'f32', data:X}, {type:'f32', data:F}, {type:'f32', data:H.zeros(h * w), read:true}],
    launches: [H.l2('conv2d', w, h, [{buf:0}, {buf:1}, {buf:2}, h, w, fh, fw])], expect: {2: e} }; };
return { cases: [mk('6 x 7, 3 x 3', 6, 7, 3, 3, 1, false), mk('20 x 23, 3 x 3 (crosses blocks)', 20, 23, 3, 3, 2, false), mk('19 x 18, 5 x 3', 19, 18, 5, 3, 3, true), mk('3 x 3, 5 x 5 (filter bigger than image)', 3, 3, 5, 5, 4, true)] };
