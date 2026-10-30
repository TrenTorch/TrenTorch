// O(n) time, O(1) space
function longestSubarraySumK(nums, k) {
  let best = 0;
  let left = 0;
  let total = 0;
  for (let right = 0; right < nums.length; right++) {
    total += nums[right];
    while (total > k && left <= right) {
      total -= nums[left];
      left++;
    }
    if (total === k) {
      best = Math.max(best, right - left + 1);
    }
  }
  return best;
}

console.log(longestSubarraySumK([1, 2, 3, 1, 1, 1, 1], 3));
