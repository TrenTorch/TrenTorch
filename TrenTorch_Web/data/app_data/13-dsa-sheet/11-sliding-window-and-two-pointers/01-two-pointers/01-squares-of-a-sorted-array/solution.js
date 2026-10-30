// O(n) time, O(n) space
function sortedSquares(nums) {
  const out = new Array(nums.length);
  let left = 0;
  let right = nums.length - 1;
  for (let i = nums.length - 1; i >= 0; i--) {
    if (Math.abs(nums[left]) > Math.abs(nums[right])) {
      out[i] = nums[left] * nums[left];
      left++;
    } else {
      out[i] = nums[right] * nums[right];
      right--;
    }
  }
  return out;
}

console.log(sortedSquares([-4, -1, 0, 3, 10]));
