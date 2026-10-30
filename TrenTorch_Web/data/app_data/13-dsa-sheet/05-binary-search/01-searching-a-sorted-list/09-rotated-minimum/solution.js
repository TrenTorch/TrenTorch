// O(log n) time, O(1) space
function rotatedMinimum(nums) {
  let lo = 0;
  let hi = nums.length - 1;
  while (lo < hi) {
    const mid = Math.floor((lo + hi) / 2);
    if (nums[mid] > nums[hi]) {
      lo = mid + 1;
    } else {
      hi = mid;
    }
  }
  return nums[lo];
}

console.log(rotatedMinimum([4, 5, 6, 7, 0, 1, 2]));
