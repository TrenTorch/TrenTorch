// O(n) time, O(1) space
function longestOnes(nums, k) {
  let zeros = 0;
  let left = 0;
  let best = 0;
  for (let right = 0; right < nums.length; right++) {
    if (nums[right] === 0) {
      zeros++;
    }
    while (zeros > k) {
      if (nums[left] === 0) {
        zeros--;
      }
      left++;
    }
    best = Math.max(best, right - left + 1);
  }
  return best;
}

console.log(longestOnes([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2));
