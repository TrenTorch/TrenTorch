// O(n) time, O(k) space
function containsNearbyDuplicate(nums, k) {
  const window = new Set();
  for (let i = 0; i < nums.length; i++) {
    const x = nums[i];
    if (window.has(x)) {
      return true;
    }
    window.add(x);
    if (i >= k) {
      window.delete(nums[i - k]);
    }
  }
  return false;
}

console.log(containsNearbyDuplicate([1, 2, 3, 1], 3));
