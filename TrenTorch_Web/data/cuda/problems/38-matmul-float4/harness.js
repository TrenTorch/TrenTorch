const mm = (A, B, M, N, K) => { const C = []; for (let i = 0; i < M; i++) for (let j = 0; j < N; j++) { let a = 0; for (let k = 0; k < K; k++) a += A[i * K + k] * B[k * N + j]; C.push(a); } return C; };
const mk = (name, M, N, K, seed, hidden) => { const A = H.rand(M * K, seed), B = H.rand(K * N, seed + 1);
  return { name, hidden, tol: {abs: 1e-4, rel: 1e-3}, buffers: [{type:'f32', data:A}, {type:'f32', data:B}, {type:'f32', data:H.zeros(M * N), read:true}],
    launches: [H.l2('matmul_vec4', N / 4, M, [{buf:0}, {buf:1}, {buf:2}, M, N, K])], expect: {2: mm(A, B, M, N, K)},
    check: (o, c) => (c.globalLoadBytes / Math.max(1, c.globalLoads) < 6 ? 'loads average ' + (c.globalLoadBytes / c.globalLoads).toFixed(1) + ' bytes: read B with float4 so a load moves 16 bytes' : null) }; };
return { cases: [mk('5 x 8 x 4', 5, 8, 4, 1, false), mk('20 x 24 x 16', 20, 24, 16, 2, false), mk('17 x 36 x 12', 17, 36, 12, 3, true)] };
