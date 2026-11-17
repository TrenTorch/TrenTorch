// O(n log n) time, O(n) space
function maxActivities(starts, ends) {
  const n = starts.length;
  const pairs = new Array(n);
  for (let i = 0; i < n; i++) {
    pairs[i] = [ends[i], starts[i]];
  }
  pairs.sort((a, b) => a[0] - b[0]);

  let count = 0;
  let lastEnd = -1;
  for (let i = 0; i < n; i++) {
    const [end, start] = pairs[i];
    if (start >= lastEnd) {
      count++;
      lastEnd = end;
    }
  }
  return count;
}

console.log(maxActivities([1, 3, 0, 5, 8, 5], [2, 4, 6, 7, 9, 9]));
