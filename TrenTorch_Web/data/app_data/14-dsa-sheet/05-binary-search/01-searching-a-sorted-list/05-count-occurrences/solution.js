// O(log n) time, O(1) space
function lowerBound(nums, target) {
  let left = 0;
  let right = nums.length;
  while (left < right) {
    const mid = Math.floor((left + right) / 2);
    if (nums[mid] < target) {
      left = mid + 1;
    } else {
      right = mid;
    }
  }
  return left;
}

function upperBound(nums, target) {
  let left = 0;
  let right = nums.length;
  while (left < right) {
    const mid = Math.floor((left + right) / 2);
    if (nums[mid] <= target) {
      left = mid + 1;
    } else {
      right = mid;
    }
  }
  return left;
}

function countOccurrences(nums, target) {
  return upperBound(nums, target) - lowerBound(nums, target);
}

console.log(countOccurrences([1, 2, 2, 2, 3], 2));
