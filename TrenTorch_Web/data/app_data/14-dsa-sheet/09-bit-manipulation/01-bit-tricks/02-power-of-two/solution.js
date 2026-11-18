// O(1) time, O(1) space
function isPowerOfTwo(n) {
  const big = BigInt(n);
  return big > 0n && (big & (big - 1n)) === 0n;
}

console.log(isPowerOfTwo(16));
