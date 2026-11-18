// O(n log n) time, O(n) space
function jobScheduling(jobs) {
  if (!jobs || jobs.length === 0) return 0;
  const items = [...jobs].sort((a, b) => a[1] - b[1]);
  const ends = items.map(j => j[1]);
  const n = items.length;
  const best = new Array(n + 1).fill(0);
  for (let i = 1; i <= n; i++) {
    const [start, end, profit] = items[i - 1];
    let lo = 0;
    let hi = i - 1;
    while (lo < hi) {
      const mid = (lo + hi) >>> 1;
      if (ends[mid] <= start) {
        lo = mid + 1;
      } else {
        hi = mid;
      }
    }
    const before = lo;
    best[i] = Math.max(best[i - 1], profit + best[before]);
  }
  return best[n];
}

console.log(jobScheduling([[1, 3, 50], [2, 4, 10], [3, 5, 40], [3, 6, 70]]));
