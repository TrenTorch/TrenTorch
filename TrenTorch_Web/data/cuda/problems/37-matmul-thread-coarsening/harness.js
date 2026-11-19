const mm = (A, B, M, N, K) => { const C = []; for (let i = 0; i < M; i++) for (let j = 0; j < N; j++) { let a = 0; for (let k = 0; k < K; k++) a += A[i * K + k] * B[k * N + j]; C.push(a); } return C; };
const mk = (name, M, N, K, seed, hidden) => { const A = H.rand(M * K, seed), B = H.rand(K * N, seed + 1);
  return { name, hidden, tol: {abs: 1e-4, rel: 1e-3}, buffers: [{type:'f32', data:A}, {type:'f32', data:B}, {type:'f32', data:H.zeros(M * N), read:true}],
    launches: [{ kernel: 'matmul_coarsened', grid: {x: Math.ceil(N / 16), y: Math.ceil(M / 16)}, block: {x: 8, y: 8}, args: [{buf:0}, {buf:1}, {buf:2}, M, N, K] }], expect: {2: mm(A, B, M, N, K)} }; };
return { cases: [mk('6 x 6 x 4', 6, 6, 4, 1, false), mk('20 x 23 x 17 (odd sizes)', 20, 23, 17, 2, false), mk('33 x 31 x 9', 33, 31, 9, 3, true)] };
