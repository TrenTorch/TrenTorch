// O(n) time, O(1) space
function missingNumber(nums) {
  const n = nums.length;
  let sum = 0;
  for (let i = 0; i < n; i++) {
    sum += nums[i];
  }
  return n * (n + 1) / 2 - sum;
}

console.log(missingNumber([3, 0, 1]));
