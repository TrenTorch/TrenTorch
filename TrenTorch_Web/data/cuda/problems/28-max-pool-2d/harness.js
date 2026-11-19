const mk = (name, h, w, ph, pw, sh, sw, seed, hidden) => { const X = H.rand(h * w, seed, -9, -1), OH = Math.floor((h - ph) / sh) + 1, OW = Math.floor((w - pw) / sw) + 1, e = [];
  for (let oy = 0; oy < OH; oy++) for (let ox = 0; ox < OW; ox++) { let m = -Infinity; for (let ky = 0; ky < ph; ky++) for (let kx = 0; kx < pw; kx++) m = Math.max(m, X[(oy * sh + ky) * w + ox * sw + kx]); e.push(m); }
  return { name, hidden, buffers: [{type:'f32', data:X}, {type:'f32', data:H.zeros(OH * OW), read:true}],
    launches: [H.l2('maxpool2d', OW, OH, [{buf:0}, {buf:1}, h, w, OH, OW, ph, pw, sh, sw])], expect: {1: e} }; };
return { cases: [mk('8 x 8, 2 x 2, stride 2', 8, 8, 2, 2, 2, 2, 1, false), mk('37 x 41, 3 x 3, stride 2 (overlapping windows)', 37, 41, 3, 3, 2, 2, 2, false), mk('20 x 33, 2 x 3, strides 1 and 3', 20, 33, 2, 3, 1, 3, 3, true)] };
