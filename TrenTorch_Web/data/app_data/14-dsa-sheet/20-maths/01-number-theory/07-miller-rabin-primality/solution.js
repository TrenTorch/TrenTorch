// O(k log^3 n) time, O(1) space where k=12 (deterministic for n < 9e15)
function isPrime(n) {
  if (n < 2) return false;
  const small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37];
  for (const p of small) {
    if (n % p === 0) return n === p;
  }
  let d = n - 1;
  let s = 0;
  while (d % 2 === 0) {
    d /= 2;
    s++;
  }
  function modPow(base, exp, mod) {
    let result = 1;
    base = base % mod;
    while (exp > 0) {
      if (exp & 1) result = (result * base) % mod;
      base = (base * base) % mod;
      exp >>= 1;
    }
    return result;
  }
  for (const a of small) {
    let x = modPow(a, d, n);
    if (x === 1 || x === n - 1) continue;
    let composite = true;
    for (let r = 1; r < s; r++) {
      x = (x * x) % n;
      if (x === n - 1) {
        composite = false;
        break;
      }
    }
    if (composite) return false;
  }
  return true;
}

console.log(isPrime(97));
