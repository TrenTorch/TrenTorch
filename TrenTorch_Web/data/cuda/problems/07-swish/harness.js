const f = x => x / (1 + Math.exp(-x));
const mk = (name, n, seed, hidden, lo, hi) => {
  const X = H.rand(n, seed, lo, hi);
  return { name, hidden, tol: {abs:1e-5,rel:1e-4}, buffers: [{type:'f32', data:X}, {type:'f32', data:H.zeros(n), read:true}],
    launches: [H.l1('swish', n, [{buf:0}, {buf:1}, n])], expect: {1: X.map(f)} };
};
return { cases: [
  mk('N = 5 (fewer threads than one block)', 5, 1, false, -5, 5),
  mk('N = 1000 (not a multiple of the block size)', 1000, 2, false, -5, 5),
  mk('N = 4099, wide value range', 4099, 3, true, -20, 20),
  mk('N = 1', 1, 4, true, -5, 5)
] };
