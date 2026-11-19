const mk = (name, n, seed, hidden) => {
  const A = H.rand(n, seed), B = H.rand(n, seed + 100);
  return { name, hidden, buffers: [{type:'f32', data:A}, {type:'f32', data:B}, {type:'f32', data:H.zeros(n), read:true}],
    launches: [H.l1('vector_add', n, [{buf:0}, {buf:1}, {buf:2}, n])], expect: {2: A.map((a, i) => a + B[i])} };
};
return { cases: [mk('N = 6 (fewer threads than one block)', 6, 1, false), mk('N = 1000 (not a multiple of 256)', 1000, 2, false), mk('N = 4096', 4096, 3, true), mk('N = 1', 1, 4, true)] };
