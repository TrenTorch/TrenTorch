// O(sqrt(n)) time, O(log n) space
function primeFactors(n) {
  const out = [];
  let d = 2;
  while (d * d <= n) {
    if (n % d === 0) {
      let e = 0;
      while (n % d === 0) {
        n = Math.floor(n / d);
        e += 1;
      }
      out.push([d, e]);
    }
    d += d === 2 ? 1 : 2;
  }
  if (n > 1) {
    out.push([n, 1]);
  }
  return out;
}

console.log(primeFactors(360));
