// O(n * target / wordSize) time, O(target / wordSize) space
function subsetSum(nums, target) {
  const t = BigInt(target);
  const mask = (1n << (t + 1n)) - 1n;
  let bits = 1n;
  for (const x of nums) {
    const bx = BigInt(x);
    bits |= (bits << bx) & mask;
  }
  return ((bits >> t) & 1n) === 1n;
}

console.log(subsetSum([3, 34, 4, 12, 5, 2], 9));
