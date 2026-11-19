const mm = (A, B, M, N, K) => { const C = []; for (let i = 0; i < M; i++) for (let j = 0; j < N; j++) { let a = 0; for (let k = 0; k < K; k++) a += A[i * K + k] * B[k * N + j]; C.push(a); } return C; };
const mk = (name, M, N, K, seed, hidden, perf) => { const A = H.rand(M * K, seed), B = H.rand(K * N, seed + 1);
  return { name, hidden, tol: {abs: 1e-4, rel: 1e-3}, buffers: [{type:'f32', data:A}, {type:'f32', data:B}, {type:'f32', data:H.zeros(M * N), read:true}],
    launches: [H.l2('matmul_tiled', N, M, [{buf:0}, {buf:1}, {buf:2}, M, N, K])], expect: {2: mm(A, B, M, N, K)},
    check: perf ? (o, c) => (c.sharedStores === 0 ? 'correct, but no shared memory is used: stage tiles of A and B' : c.globalLoads > 0.25 * 2 * M * N * K ? 'correct, but ' + c.globalLoads + ' global loads is not below a quarter of the naive ' + 2 * M * N * K + ': reuse each tile across the block' : null) : null }; };
return { cases: [mk('5 x 7 x 3 (smaller than a tile)', 5, 7, 3, 1, false, false), mk('20 x 24 x 17 (edge tiles)', 20, 24, 17, 2, false, false), mk('32 x 32 x 32 reuse check', 32, 32, 32, 3, true, true)] };
