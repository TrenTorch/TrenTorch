// O(log n) time, O(log n) space
function nthFibonacci(n) {
  function fib(k) {
    if (k === 0) {
      return [0n, 1n];
    }
    const [a, b] = fib(k >> 1);
    const c = a * (2n * b - a);
    const d = a * a + b * b;
    return (k & 1) ? [d, c + d] : [c, d];
  }
  return fib(n)[0].toString();
}

console.log(nthFibonacci(10));
