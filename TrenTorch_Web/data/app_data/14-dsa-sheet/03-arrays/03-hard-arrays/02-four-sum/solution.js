function fourSum(nums, target) {
  // O(n^3) time, O(1) space (excluding output)
  const a = nums.slice().sort((x, y) => x - y);
  const n = a.length;
  const out = [];
  for (let i = 0; i < n - 3; i++) {
    if (i > 0 && a[i] === a[i - 1]) continue;
    for (let j = i + 1; j < n - 2; j++) {
      if (j > i + 1 && a[j] === a[j - 1]) continue;
      let lo = j + 1;
      let hi = n - 1;
      while (lo < hi) {
        const total = a[i] + a[j] + a[lo] + a[hi];
        if (total < target) {
          lo++;
        } else if (total > target) {
          hi--;
        } else {
          out.push([a[i], a[j], a[lo], a[hi]]);
          lo++;
          hi--;
          while (lo < hi && a[lo] === a[lo - 1]) lo++;
          while (lo < hi && a[hi] === a[hi + 1]) hi--;
        }
      }
    }
  }
  return out;
}

console.log(fourSum([1, 0, -1, 0, -2, 2], 0));
