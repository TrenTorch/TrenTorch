// O(n) time, O(1) space
function wiggleLength(nums) {
  if (!nums || nums.length === 0) {
    return 0;
  }
  let length = 1;
  let direction = 0;
  for (let i = 1; i < nums.length; i++) {
    const diff = nums[i] - nums[i - 1];
    if (diff > 0 && direction <= 0) {
      length++;
      direction = 1;
    } else if (diff < 0 && direction >= 0) {
      length++;
      direction = -1;
    }
  }
  return length;
}

console.log(wiggleLength([1, 7, 4, 9, 2, 5]));
