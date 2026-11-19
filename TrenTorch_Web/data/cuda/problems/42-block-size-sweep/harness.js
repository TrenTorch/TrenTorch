const n = 3000, a = 2.5, x = H.rand(n, 1), y = H.rand(n, 2), e = y.map((v, i) => a * x[i] + v);
const mk = (block, grid, hidden) => ({ name: 'block ' + block + ', ' + grid + ' blocks', hidden, tol: {abs: 1e-5, rel: 1e-4},
  buffers: [{type:'f32', data:x}, {type:'f32', data:y, read:true}], launches: [{ kernel: 'saxpy_any_block', grid, block, args: [a, {buf:0}, {buf:1}, n] }], expect: {1: e} });
return { cases: [mk(32, Math.ceil(n / 32), false), mk(64, Math.ceil(n / 64), false), mk(128, Math.ceil(n / 128), true), mk(256, Math.ceil(n / 256), true), mk(512, Math.ceil(n / 512), true), mk(1024, Math.ceil(n / 1024), true), mk(128, 3, true)] };
