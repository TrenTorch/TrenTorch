// O(n^2) time, O(n^2) space
function minCostCut(length, cuts) {
  const points = [0, ...cuts.slice().sort((a, b) => a - b), length];
  const n = points.length;
  const dp = Array.from({ length: n }, () => Array(n).fill(0));
  const bestCut = Array.from({ length: n }, () => Array(n).fill(0));

  for (let i = 0; i < n - 1; i++) {
    bestCut[i][i + 1] = i + 1;
  }

  for (let span = 2; span < n; span++) {
    for (let i = 0; i + span < n; i++) {
      const j = i + span;
      let low = Math.max(i + 1, bestCut[i][j - 1]);
      let high = Math.min(j - 1, bestCut[i + 1][j]);
      let best = null;
      let bestK = low;
      for (let k = low; k <= high; k++) {
        const value = dp[i][k] + dp[k][j];
        if (best === null || value < best) {
          best = value;
          bestK = k;
        }
      }
      bestCut[i][j] = bestK;
      dp[i][j] = best + points[j] - points[i];
    }
  }

  return dp[0][n - 1];
}

console.log(minCostCut(7, [1, 3, 4, 5]));
