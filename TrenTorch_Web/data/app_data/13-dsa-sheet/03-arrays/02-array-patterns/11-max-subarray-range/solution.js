// O(n) time, O(1) space
function maxSubarrayRange(nums) {
  let best = [nums[0], 0, 0];
  let current = nums[0];
  let begin = 0;
  for (let i = 1; i < nums.length; i++) {
    if (current < 0) {
      current = nums[i];
      begin = i;
    } else {
      current += nums[i];
    }
    if (current > best[0]) {
      best = [current, begin, i];
    }
  }
  return best;
}

console.log(maxSubarrayRange([-2, 1, -3, 4, -1, 2, 1, -5, 4]));
