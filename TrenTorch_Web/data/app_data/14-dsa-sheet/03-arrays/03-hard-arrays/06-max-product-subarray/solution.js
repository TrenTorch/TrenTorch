// O(n) time, O(1) space
function maxProductSubarray(nums) {
  let best = nums[0];
  let hi = nums[0];
  let lo = nums[0];
  for (let i = 1; i < nums.length; i++) {
    const x = nums[i];
    const candidates = [x, hi * x, lo * x];
    hi = Math.max(...candidates);
    lo = Math.min(...candidates);
    if (hi > best) best = hi;
  }
  return best;
}

console.log(maxProductSubarray([2, 3, -2, 4]));
