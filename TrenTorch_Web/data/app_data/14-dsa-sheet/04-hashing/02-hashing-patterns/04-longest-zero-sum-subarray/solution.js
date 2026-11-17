// O(n) time, O(n) space
function longestZeroSumSubarray(nums) {
  const first = new Map();
  first.set(0, -1);
  let prefix = 0;
  let best = 0;
  for (let i = 0; i < nums.length; i++) {
    prefix += nums[i];
    if (first.has(prefix)) {
      best = Math.max(best, i - first.get(prefix));
    } else {
      first.set(prefix, i);
    }
  }
  return best;
}

console.log(longestZeroSumSubarray([15, -2, 2, -8, 1, 7, 10, 23]));
