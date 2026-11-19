const mk = (name, n, seed, hidden) => {
  const A = H.rand(n, seed, -4, 4), B = H.rand(n, seed + 7, -4, 4);
  return { name, hidden, buffers: [{type:'f32', data:A}, {type:'f32', data:B}, {type:'f32', data:H.zeros(n), read:true}],
    launches: [H.l1('hadamard', n, [{buf:0}, {buf:1}, {buf:2}, n])], expect: {2: A.map((a, i) => a * B[i])} };
};
return { cases: [mk('N = 7', 7, 1, false), mk('N = 999', 999, 2, false), mk('N = 4100', 4100, 3, true)] };
