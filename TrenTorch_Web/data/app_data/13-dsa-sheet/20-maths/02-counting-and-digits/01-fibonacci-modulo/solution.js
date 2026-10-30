// O(log n) time, O(log n) space
const MOD = 1000000007n;

function fibMod(n) {
  function pair(k) {
    if (k === 0) {
      return [0n, 1n];
    }
    const [a, b] = pair(Math.floor(k / 2));
    const twoBMinusA = (2n * b - a) % MOD;
    const c = (a * ((twoBMinusA + MOD) % MOD)) % MOD;
    const e = (a * a + b * b) % MOD;
    if (k % 2 === 0) {
      return [c, e];
    } else {
      return [e, (c + e) % MOD];
    }
  }
  return Number(pair(n)[0]);
}

console.log(fibMod(10));
