// O(log n) time, O(1) space
function floorAndCeil(nums, target) {
  let lo = 0, hi = nums.length;
  while (lo < hi) {
    let mid = Math.floor((lo + hi) / 2);
    if (nums[mid] < target) {
      lo = mid + 1;
    } else {
      hi = mid;
    }
  }
  let ceil = (lo < nums.length) ? nums[lo] : -1;
  let floor;
  if (lo < nums.length && nums[lo] === target) {
    floor = target;
  } else {
    floor = (lo > 0) ? nums[lo - 1] : -1;
  }
  return [floor, ceil];
}

console.log(floorAndCeil([1, 2, 8, 10, 11, 12, 19], 5));
