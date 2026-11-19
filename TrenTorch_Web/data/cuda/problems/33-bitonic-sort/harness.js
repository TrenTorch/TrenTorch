const mk = (name, n, seed, hidden, real) => { const keys = H.rand(real || n, seed, -50, 50); const data = keys.slice(); while (data.length < n) data.push(1e30);
  const e = data.slice().sort((a, b) => a - b); const launches = [];
  for (let k = 2; k <= n; k *= 2) for (let j = k / 2; j > 0; j = Math.floor(j / 2)) launches.push(H.l1('bitonic_step', n, [{buf:0}, j, k, n]));
  return { name, hidden, buffers: [{type:'f32', data:data, read:true}], launches, expect: {0: e} }; };
return { cases: [mk('n = 8', 8, 1, false), mk('n = 256', 256, 2, false), mk('1000 keys padded to 1024', 1024, 3, true, 1000), mk('n = 512, many duplicates', 512, 4, true)] };
