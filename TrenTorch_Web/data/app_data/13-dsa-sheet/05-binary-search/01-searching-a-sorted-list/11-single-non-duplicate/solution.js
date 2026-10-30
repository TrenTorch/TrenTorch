// O(log n) time, O(1) space
function singleNonDuplicate(nums) {
  let lo = 0;
  let hi = nums.length - 1;
  while (lo < hi) {
    let mid = Math.floor((lo + hi) / 2);
    if (mid % 2 === 1) {
      mid -= 1;
    }
    if (nums[mid] === nums[mid + 1]) {
      lo = mid + 2;
    } else {
      hi = mid;
    }
  }
  return nums[lo];
}

console.log(singleNonDuplicate([1, 1, 2, 3, 3, 4, 4, 8, 8]));
