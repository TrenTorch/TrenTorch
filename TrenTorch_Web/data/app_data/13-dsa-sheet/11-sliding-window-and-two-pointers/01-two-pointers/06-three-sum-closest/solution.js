// O(n^2) time, O(n) space
function threeSumClosest(nums, target) {
  const a = [...nums].sort((x, y) => x - y);
  let best = a[0] + a[1] + a[2];
  for (let i = 0; i < a.length - 2; i++) {
    let lo = i + 1;
    let hi = a.length - 1;
    while (lo < hi) {
      const s = a[i] + a[lo] + a[hi];
      const diff = Math.abs(s - target);
      const bestDiff = Math.abs(best - target);
      if (diff < bestDiff || (diff === bestDiff && s < best)) {
        best = s;
      }
      if (s < target) {
        lo++;
      } else if (s > target) {
        hi--;
      } else {
        return s;
      }
    }
  }
  return best;
}

console.log(threeSumClosest([-1, 2, 1, -4], 1));
