// O(log n) time, O(1) space
function countSetBits(n) {
  let count = 0;
  let val = BigInt(n);
  while (val > 0n) {
    val &= val - 1n;
    count++;
  }
  return count;
}

console.log(countSetBits(13));
