// O(n) time, O(n) space
function countSubarraysSumK(nums, k) {
  const seen = new Map();
  seen.set(0, 1);
  let prefix = 0;
  let count = 0;
  for (const x of nums) {
    prefix += x;
    count += seen.get(prefix - k) || 0;
    seen.set(prefix, (seen.get(prefix) || 0) + 1);
  }
  return count;
}

console.log(countSubarraysSumK([1, 1, 1], 2));
