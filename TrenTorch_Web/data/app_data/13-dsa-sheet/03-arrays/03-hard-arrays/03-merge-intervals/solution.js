// O(n log n) time, O(n) space
function mergeIntervals(intervals) {
  const sorted = intervals.slice().sort((a, b) => a[0] - b[0]);
  const out = [];
  for (const [start, end] of sorted) {
    if (out.length > 0 && start <= out[out.length - 1][1]) {
      out[out.length - 1][1] = Math.max(out[out.length - 1][1], end);
    } else {
      out.push([start, end]);
    }
  }
  return out;
}

console.log(mergeIntervals([[1, 3], [8, 10], [2, 6], [15, 18]]));
