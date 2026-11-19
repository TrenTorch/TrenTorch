const N = 4000, X = H.rand(N, 5, 1, 2);
const run = (p, seed) => H.l1('dropout_hash', N, [{buf:0}, {buf:1}, N, p, seed]);
const frac = (o) => o.filter((v) => v !== 0).length / N;
const scaled = (o, p) => o.every((v, i) => v === 0 || Math.abs(v - X[i] / p) < 1e-4);
const base = (extra) => Object.assign({ buffers: [{type:'f32', data:X}, {type:'f32', data:H.zeros(N), read:true}, {type:'f32', data:H.zeros(N), read:true}] }, extra);
return { cases: [
  base({ name: 'keep_prob = 1 returns the input', launches: [run(1, 7)], expect: {1: X} }),
  base({ name: 'keep_prob = 0.5 keeps about half and scales by 2', launches: [run(0.5, 11)],
    check: (o) => (Math.abs(frac(o[1]) - 0.5) > 0.2 ? 'kept fraction is ' + frac(o[1]).toFixed(2) + ', expected about 0.5' : !scaled(o[1], 0.5) ? 'a kept value is not X[i] / keep_prob' : null) }),
  base({ name: 'same seed, same mask', hidden: true,
    launches: [run(0.7, 3), { kernel: 'dropout_hash', grid: Math.ceil(N / 256), block: 256, args: [{buf:0}, {buf:2}, N, 0.7, 3] }],
    check: (o) => (o[1].some((v, i) => v !== o[2][i]) ? 'the same seed produced two different masks' : Math.abs(frac(o[1]) - 0.7) > 0.2 ? 'kept fraction is ' + frac(o[1]).toFixed(2) + ', expected about 0.7' : null) }),
  base({ name: 'keep_prob = 0 returns zeros', hidden: true, launches: [run(0, 9)], expect: {1: H.zeros(N)} })
] };
