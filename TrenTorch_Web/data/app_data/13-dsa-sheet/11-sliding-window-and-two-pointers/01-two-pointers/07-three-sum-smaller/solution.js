// O(n log n) time, O(1) extra space
function countTripletsSmaller(nums, target) {
  const a = nums.slice().sort((x, y) => x - y);
  let count = 0;
  for (let i = 0; i < a.length - 2; i++) {
    let lo = i + 1;
    let hi = a.length - 1;
    while (lo < hi) {
      if (a[i] + a[lo] + a[hi] < target) {
        count += hi - lo;
        lo++;
      } else {
        hi--;
      }
    }
  }
  return count;
}

console.log(countTripletsSmaller([-2, 0, 1, 3], 2));
