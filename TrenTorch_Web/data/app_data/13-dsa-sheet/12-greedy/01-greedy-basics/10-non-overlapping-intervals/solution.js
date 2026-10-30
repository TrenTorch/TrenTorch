// O(n log n) time, O(1) extra space
function eraseOverlap(intervals) {
  let removed = 0;
  let lastEnd = null;
  intervals.sort((a, b) => a[1] - b[1]);
  for (const [start, end] of intervals) {
    if (lastEnd === null || start >= lastEnd) {
      lastEnd = end;
    } else {
      removed += 1;
    }
  }
  return removed;
}

console.log(eraseOverlap([[1, 2], [2, 3], [3, 4], [1, 3]]));
