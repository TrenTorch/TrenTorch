// O(n) time, O(n) space
function countBitsUpTo(n) {
  const bits = new Array(n + 1).fill(0);
  for (let i = 1; i <= n; i++) {
    bits[i] = bits[i >> 1] + (i & 1);
  }
  return bits;
}

console.log(countBitsUpTo(5));
