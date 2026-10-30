// O(k log MOD) time, O(1) space
function binomialMod(n, k) {
  const MOD = 1000000007n;
  if (k < 0 || k > n) return 0;
  const kk = Math.min(k, n - k);
  let num = 1n;
  let den = 1n;
  const bigN = BigInt(n);
  for (let i = 0; i < kk; i++) {
    num = (num * ((bigN - BigInt(i)) % MOD)) % MOD;
    den = (den * BigInt(i + 1)) % MOD;
  }
  const invDen = modPow(den, MOD - 2n, MOD);
  const result = (num * invDen) % MOD;
  return Number(result);
}

function modPow(base, exponent, mod) {
  let result = 1n;
  let b = base % mod;
  let e = exponent;
  while (e > 0n) {
    if (e & 1n) result = (result * b) % mod;
    b = (b * b) % mod;
    e >>= 1n;
  }
  return result;
}

console.log(binomialMod(5, 2));
