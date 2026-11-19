const mk = (name, h, w, seed, hidden) => { const n = h * w, A = H.rand(n, seed), B = H.rand(n, seed + 5);
  return { name, hidden, buffers: [{type:'f32', data:A}, {type:'f32', data:B}, {type:'f32', data:H.zeros(n), read:true}],
    launches: [H.l2('matrix_add', w, h, [{buf:0}, {buf:1}, {buf:2}, h, w], 32, 8)], expect: {2: A.map((a, i) => a + B[i])} }; };
return { cases: [mk('3 x 5', 3, 5, 1, false), mk('20 x 45 (edges are not multiples of the block)', 20, 45, 2, false), mk('33 x 70', 33, 70, 3, true)] };
