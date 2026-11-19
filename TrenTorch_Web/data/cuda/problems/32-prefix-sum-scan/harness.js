const mk = (name, n, seed, hidden) => { const x = H.ints(n, seed, 0, 9); const e = []; let a = 0; x.forEach((v) => { a += v; e.push(a); }); const nb = Math.ceil(n / 256);
  return { name, hidden, buffers: [{type:'f32', data:x}, {type:'f32', data:H.zeros(n), read:true}, {type:'f32', data:H.zeros(nb)}],
    launches: [H.l1('scan_blocks', n, [{buf:0}, {buf:1}, {buf:2}, n], 256, 1024), { kernel: 'scan_sums', grid: 1, block: 32, args: [{buf:2}, nb] }, H.l1('add_offsets', n, [{buf:1}, {buf:2}, n])], expect: {1: e} }; };
return { cases: [mk('n = 100 (one block)', 100, 1, false), mk('n = 1000 (4 blocks)', 1000, 2, false), mk('n = 5000 (20 blocks)', 5000, 3, true), mk('n = 256 (exactly one block)', 256, 4, true)] };
