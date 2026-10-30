// O(log n) time, O(1) space
function upperBound(nums, target) {
  let lo = 0, hi = nums.length;
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (nums[mid] <= target) {
      lo = mid + 1;
    } else {
      hi = mid;
    }
  }
  return lo;
}

console.log(upperBound([1, 2, 2, 2, 5], 2));
