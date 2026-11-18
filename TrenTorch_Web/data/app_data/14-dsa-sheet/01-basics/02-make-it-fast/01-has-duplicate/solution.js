// O(n) time, O(n) space
function hasDuplicate(nums) {
  const seen = new Set();
  for (const x of nums) {
    if (seen.has(x)) {
      return true;
    }
    seen.add(x);
  }
  return false;
}

console.log(hasDuplicate([1, 2, 3, 1]));
