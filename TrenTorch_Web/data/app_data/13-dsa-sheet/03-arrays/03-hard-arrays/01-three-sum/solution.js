// O(n log n) time, O(1) extra space (output size excluded)
function threeSum(nums) {
  const a = nums.slice().sort((x, y) => x - y);
  const out = [];
  const n = a.length;
  for (let i = 0; i < n - 2; i++) {
    if (i > 0 && a[i] === a[i - 1]) continue;
    let lo = i + 1;
    let hi = n - 1;
    while (lo < hi) {
      const total = a[i] + a[lo] + a[hi];
      if (total < 0) {
        lo++;
      } else if (total > 0) {
        hi--;
      } else {
        out.push([a[i], a[lo], a[hi]]);
        lo++;
        hi--;
        while (lo < hi && a[lo] === a[lo - 1]) lo++;
        while (lo < hi && a[hi] === a[hi + 1]) hi--;
      }
    }
  }
  return out;
}

console.log(threeSum([-1, 0, 1, 2, -1, -4]));
