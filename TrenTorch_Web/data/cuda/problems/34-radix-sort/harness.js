const mk = (name, n, seed, hidden) => { const keys = H.ints(n, seed, 0, 1023); const e = keys.slice().sort((a, b) => a - b); const launches = [];
  for (let bit = 0; bit < 10; bit++) launches.push({ kernel: 'radix_pass', grid: 1, block: 1024, args: [{buf: bit % 2}, {buf: (bit + 1) % 2}, n, bit] });
  return { name, hidden, buffers: [{type:'i32', data:keys, read:true}, {type:'i32', data:H.zeros(n)}], launches, expect: {0: e} }; };
return { cases: [mk('n = 20', 20, 1, false), mk('n = 700', 700, 2, false), mk('n = 1024', 1024, 3, true), mk('n = 300 with many duplicates', 300, 4, true)] };
