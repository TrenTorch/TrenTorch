// O(n * sum) time, O(sum) space
function minSubsetDifference(nums) {
  let total = 0;
  for (const x of nums) total += x;
  let bits = 1n;
  for (const x of nums) {
    bits |= bits << BigInt(x);
  }
  for (let s = Math.floor(total / 2); s >= 0; s--) {
    if ((bits >> BigInt(s)) & 1n) {
      return total - 2 * s;
    }
  }
  return total;
}

console.log(minSubsetDifference([1, 6, 11, 5]));
