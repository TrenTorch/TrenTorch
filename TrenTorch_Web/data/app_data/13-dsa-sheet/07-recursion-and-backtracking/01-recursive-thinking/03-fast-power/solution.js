function powerMod(base, exp, mod) {
  // O(log exp) time, O(1) space
  let result = 1 % mod;
  base %= mod;
  while (exp > 0) {
    if (exp & 1) {
      result = (result * base) % mod;
    }
    base = (base * base) % mod;
    exp >>= 1;
  }
  return result;
}

console.log(powerMod(2, 10, 1000));
