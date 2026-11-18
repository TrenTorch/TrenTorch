// O(n^2) time, O(n) space
function rodCutting(prices, length) {
  const best = new Array(length + 1).fill(0);
  for (let n = 1; n <= length; n++) {
    for (let k = 1; k <= n; k++) {
      const candidate = prices[k - 1] + best[n - k];
      if (candidate > best[n]) {
        best[n] = candidate;
      }
    }
  }
  return best[length];
}

console.log(rodCutting([1, 5, 8, 9, 10, 17, 17, 20], 8));
