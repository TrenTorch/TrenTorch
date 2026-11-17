// O(1) time, O(1) space
function isPowerOfFour(n) {
  const N = typeof n === 'bigint' ? n : BigInt(n);
  return N > 0n && (N & (N - 1n)) === 0n && (N & 0x5555555555555555n) !== 0n;
}

console.log(isPowerOfFour(16));
