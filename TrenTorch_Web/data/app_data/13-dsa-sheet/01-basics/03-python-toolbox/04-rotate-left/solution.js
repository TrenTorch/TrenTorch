// O(n) time, O(n) space
function rotateLeft(nums, k) {
  if (nums.length === 0) {
    return [];
  }
  k %= nums.length;
  return nums.slice(k).concat(nums.slice(0, k));
}

console.log(rotateLeft([1, 2, 3, 4, 5], 2));
