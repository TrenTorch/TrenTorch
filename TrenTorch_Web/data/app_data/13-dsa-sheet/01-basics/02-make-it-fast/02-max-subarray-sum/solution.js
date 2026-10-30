// O(n) time, O(1) space
function maxSubarraySum(nums) {
  let best = nums[0];
  let cur = nums[0];
  for (let i = 1; i < nums.length; i++) {
    const x = nums[i];
    cur = Math.max(x, cur + x);
    best = Math.max(best, cur);
  }
  return best;
}

console.log(maxSubarraySum([-2, 1, -3, 4, -1, 2, 1, -5, 4]));
