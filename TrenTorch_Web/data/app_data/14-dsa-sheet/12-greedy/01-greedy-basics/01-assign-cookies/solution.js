// O(n log n) time, O(n) space
function assignCookies(greed, sizes) {
  const g = greed.slice().sort((a, b) => a - b);
  const sortedSizes = sizes.slice().sort((a, b) => a - b);
  let child = 0;
  for (const cookie of sortedSizes) {
    if (child < g.length && g[child] <= cookie) {
      child++;
    }
  }
  return child;
}

console.log(assignCookies([1, 2, 3], [1, 1]));
