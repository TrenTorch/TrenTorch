const mk = (name, n, seed, hidden, ties) => { const X = H.rand(n, seed, -5, 5); let best = 0;
  ties.forEach((i) => { X[i] = 9; });
  for (let i = 0; i < n; i++) if (X[i] > X[best]) best = i;
  const blocks = Math.ceil(n / 256);
  return { name, hidden, buffers: [{type:'f32', data:X}, {type:'f32', data:H.zeros(blocks)}, {type:'i32', data:H.zeros(blocks)}, {type:'i32', data:[-1], read:true}],
    launches: [H.l1('argmax_partials', n, [{buf:0}, {buf:1}, {buf:2}, n]), { kernel: 'argmax_final', grid: 1, block: 32, args: [{buf:1}, {buf:2}, {buf:3}, blocks] }], expect: {3: [best]} }; };
return { cases: [mk('N = 1000, one maximum', 1000, 1, false, [613]), mk('ties across blocks: answer is the smallest index', 1000, 2, false, [900, 300, 7]), mk('N = 6000, tie inside one block', 6000, 3, true, [5000, 4999]), mk('N = 5', 5, 4, true, [3])] };
