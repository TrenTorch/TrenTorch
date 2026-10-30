// O(n^3) time, O(n^2) space
function matrixChainCost(dims) {
  const n = dims.length;
  if (n < 3) return 0;
  const dp = Array.from({ length: n }, () => Array(n).fill(0));
  for (let length = 2; length < n; length++) {
    for (let i = 0; i < n - length; i++) {
      const j = i + length;
      let best = Infinity;
      for (let k = i + 1; k < j; k++) {
        const value = dp[i][k] + dp[k][j] + dims[i] * dims[k] * dims[j];
        if (value < best) best = value;
      }
      dp[i][j] = best;
    }
  }
  return dp[0][n - 1];
}

console.log(matrixChainCost([10, 30, 5, 60]));
