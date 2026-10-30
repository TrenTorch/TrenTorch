// O(1) time, O(1) space
function xorOfRange(left, right) {
  function prefix(n) {
    if (n < 0) return 0;
    const r = n % 4;
    if (r === 0) return n;
    if (r === 1) return 1;
    if (r === 2) return n + 1;
    return 0;
  }
  const a = prefix(right);
  const b = prefix(left - 1);
  return Number(BigInt(a) ^ BigInt(b));
}

console.log(xorOfRange(3, 9));
