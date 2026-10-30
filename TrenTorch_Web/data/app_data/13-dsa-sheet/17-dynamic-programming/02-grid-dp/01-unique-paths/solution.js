// O(n) time, O(n) space
function uniquePaths(rows, cols) {
  const MOD = 1000000007n;
  const total = rows + cols - 2;
  const choose = rows - 1;
  const fact = new Array(total + 1);
  fact[0] = 1n;
  for (let i = 1; i <= total; i++) {
    fact[i] = (fact[i - 1] * BigInt(i)) % MOD;
  }
  function modPow(base, exp) {
    let result = 1n;
    let b = base % MOD;
    let e = exp;
    while (e > 0) {
      if (e & 1n) result = (result * b) % MOD;
      b = (b * b) % MOD;
      e >>= 1n;
    }
    return result;
  }
  function modInv(x) {
    return modPow(x, MOD - 2n);
  }
  const numerator = fact[total];
  const denominator = (fact[choose] * fact[total - choose]) % MOD;
  const ans = (numerator * modInv(denominator)) % MOD;
  return Number(ans);
}

console.log(uniquePaths(3, 7));
