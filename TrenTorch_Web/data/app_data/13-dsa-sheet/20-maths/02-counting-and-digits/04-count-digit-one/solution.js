// O(log n) time, O(1) space
function countDigitOne(n) {
  let total = 0;
  let p = 1;
  while (p <= n) {
    const high = Math.floor(n / (p * 10));
    const cur = Math.floor(n / p) % 10;
    const low = n % p;
    total += high * p;
    if (cur > 1) {
      total += p;
    } else if (cur === 1) {
      total += low + 1;
    }
    p *= 10;
  }
  return total;
}

console.log(countDigitOne(13));
