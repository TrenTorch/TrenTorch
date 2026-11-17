// O(sqrt(n)) time, O(1) space
function eulerPhi(n) {
  let result = n;
  let d = 2;
  while (d * d <= n) {
    if (n % d === 0) {
      while (n % d === 0) {
        n = Math.floor(n / d);
      }
      result -= Math.floor(result / d);
    }
    d += (d === 2) ? 1 : 2;
  }
  if (n > 1) {
    result -= Math.floor(result / n);
  }
  return result;
}

console.log(eulerPhi(12));
