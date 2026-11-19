// high-accuracy erf (Abramowitz-Stegun 7.1.26 has 1.5e-7 error; refine with a Taylor series for small |x|)
const erf = (x) => { const ax = Math.abs(x); let r;
  if (ax < 2.5) { let term = ax, sum = ax; for (let n = 1; n < 60; n++) { term *= -ax * ax / n; sum += term / (2 * n + 1); } r = 2 / Math.sqrt(Math.PI) * sum; }
  else { const t = 1 / (1 + 0.3275911 * ax); r = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-ax * ax); }
  return x < 0 ? -r : r; };
const f = (x) => 0.5 * x * (1 + erf(x / Math.SQRT2));
const mk = (name, n, seed, hidden, lo, hi) => { const X = H.rand(n, seed, lo, hi);
  return { name, hidden, tol: {abs: 2e-5, rel: 1e-4}, buffers: [{type:'f32', data:X}, {type:'f32', data:H.zeros(n), read:true}],
    launches: [H.l1('gelu_exact', n, [{buf:0}, {buf:1}, n])], expect: {1: X.map(f)} }; };
return { cases: [mk('N = 9', 9, 1, false, -3, 3), mk('N = 1000', 1000, 2, false, -4, 4), mk('N = 2051, wide range', 2051, 3, true, -8, 8)] };
