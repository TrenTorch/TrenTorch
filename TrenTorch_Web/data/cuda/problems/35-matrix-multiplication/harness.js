const mm = (A, B, M, N, K) => { const C = []; for (let i = 0; i < M; i++) for (let j = 0; j < N; j++) { let a = 0; for (let k = 0; k < K; k++) a += A[i * K + k] * B[k * N + j]; C.push(a); } return C; };
const mk = (name, M, N, K, seed, hidden) => { const A = H.rand(M * K, seed), B = H.rand(K * N, seed + 1);
  return { name, hidden, tol: {abs: 1e-4, rel: 1e-3}, buffers: [{type:'f32', data:A}, {type:'f32', data:B}, {type:'f32', data:H.zeros(M * N), read:true}],
    launches: [H.l2('matmul_naive', N, M, [{buf:0}, {buf:1}, {buf:2}, M, N, K])], expect: {2: mm(A, B, M, N, K)} }; };
return { cases: [mk('5 x 7 x 3', 5, 7, 3, 1, false), mk('20 x 24 x 17', 20, 24, 17, 2, false), mk('33 x 18 x 40', 33, 18, 40, 3, true)] };
