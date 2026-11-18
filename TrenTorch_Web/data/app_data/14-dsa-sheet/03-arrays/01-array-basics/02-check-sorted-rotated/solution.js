// O(n) time, O(1) space
function checkSortedRotated(nums) {
  const n = nums.length;
  let drops = 0;
  for (let i = 0; i < n; i++) {
    if (nums[i] > nums[(i + 1) % n]) {
      drops++;
      if (drops > 1) break;
    }
  }
  return drops <= 1;
}

console.log(checkSortedRotated([3, 4, 5, 1, 2]));
