// O(log n) time, O(1) space
function binarySearchIndex(nums, target) {
  let lo = 0;
  let hi = nums.length - 1;
  while (lo <= hi) {
    const mid = Math.floor((lo + hi) / 2);
    if (nums[mid] === target) {
      return mid;
    }
    if (nums[mid] < target) {
      lo = mid + 1;
    } else {
      hi = mid - 1;
    }
  }
  return -1;
}

console.log(binarySearchIndex([-1, 0, 3, 5, 9, 12], 9));
