const mk = (name, M, N, seed, hidden) => { const a = H.rand(M, seed), b = H.rand(N, seed + 3), e = [];
  for (let i = 0; i < M; i++) for (let j = 0; j < N; j++) e.push(a[i] * b[j]);
  return { name, hidden, buffers: [{type:'f32', data:a}, {type:'f32', data:b}, {type:'f32', data:H.zeros(M * N), read:true}],
    launches: [H.l2('outer_product', N, M, [{buf:0}, {buf:1}, {buf:2}, M, N])], expect: {2: e} }; };
return { cases: [mk('M=3, N=4', 3, 4, 1, false), mk('M=17, N=40', 17, 40, 2, false), mk('M=33, N=19', 33, 19, 3, true)] };
