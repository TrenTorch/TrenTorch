// O(n) time, O(1) space
function numberOfSubarrays(nums, k) {
  function atMost(m) {
    if (m < 0) return 0;
    let odd = 0;
    let left = 0;
    let total = 0;
    for (let right = 0; right < nums.length; right++) {
      odd += nums[right] % 2;
      while (odd > m) {
        odd -= nums[left] % 2;
        left++;
      }
      total += right - left + 1;
    }
    return total;
  }
  return atMost(k) - atMost(k - 1);
}

console.log(numberOfSubarrays([1, 1, 2, 1, 1], 3));
