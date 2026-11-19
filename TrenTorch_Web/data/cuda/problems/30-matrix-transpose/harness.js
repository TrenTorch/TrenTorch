const mk = (name, h, w, seed, hidden, perf) => { const A = H.rand(h * w, seed), e = new Array(h * w);
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) e[x * h + y] = A[y * w + x];
  return { name, hidden, buffers: [{type:'f32', data:A}, {type:'f32', data:H.zeros(h * w), read:true}],
    launches: [H.l2('transpose', w, h, [{buf:0}, {buf:1}, h, w], 32, 32)], expect: {1: e},
    check: perf ? (o, c) => (c.coalescingEfficiency < 0.85 ? 'correct, but coalescing efficiency is only ' + (c.coalescingEfficiency * 100).toFixed(0) + '% (need 85%): stage the tile in shared memory so global writes are unit-stride' : c.bankConflicts > 0 ? 'correct, but the shared tile has ' + c.bankConflicts + ' bank-conflict replays: pad it to [32][33]' : null) : null }; };
return { cases: [mk('5 x 7', 5, 7, 1, false, false), mk('40 x 70 (edge tiles)', 40, 70, 2, false, false), mk('64 x 64 efficiency check', 64, 64, 3, true, true)] };
