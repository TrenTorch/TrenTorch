// O(n) time, O(n) space
function longestSubarraySumKAny(nums, k) {
  const first = new Map();
  first.set(0, -1);
  let prefix = 0;
  let best = 0;
  for (let i = 0; i < nums.length; i++) {
    prefix += nums[i];
    if (first.has(prefix - k)) {
      best = Math.max(best, i - first.get(prefix - k));
    }
    if (!first.has(prefix)) {
      first.set(prefix, i);
    }
  }
  return best;
}

console.log(longestSubarraySumKAny([1, -1, 5, -2, 3], 3));
