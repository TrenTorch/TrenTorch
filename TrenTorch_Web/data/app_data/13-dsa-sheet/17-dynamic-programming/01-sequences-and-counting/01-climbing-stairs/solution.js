// O(log n) time, O(log n) space
function climbStairs(n) {
  const MOD = 1000000007n;
  function fib(k) {
    if (k === 0) return [0n, 1n];
    const [a, b] = fib(k >> 1);
    const twoBminusA = (2n * b - a) % MOD;
    const c = (a * (twoBminusA < 0 ? twoBminusA + MOD : twoBminusA)) % MOD;
    const d = (a * a + b * b) % MOD;
    if (k & 1) {
      return [d, (c + d) % MOD];
    } else {
      return [c, d];
    }
  }
  return Number(fib(n + 1)[0]);
}

console.log(climbStairs(3));
