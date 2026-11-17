// O(n * sum) time, O(sum) space
function canPartition(nums) {
  const total = nums.reduce((a, b) => a + b, 0);
  if (total % 2 !== 0) return false;
  const target = total / 2;
  let bits = 1n;
  for (const x of nums) {
    bits |= bits << BigInt(x);
  }
  return (bits >> BigInt(target) & 1n) === 1n;
}

console.log(canPartition([1, 5, 11, 5]));
