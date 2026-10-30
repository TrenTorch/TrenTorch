// O(n^3) time, O(n^2) space
function maxCoins(nums) {
  const a = [1].concat(nums, [1]);
  const n = a.length;
  const dp = Array.from({ length: n }, () => Array(n).fill(0));
  for (let length = 2; length < n; length++) {
    for (let i = 0; i + length < n; i++) {
      const j = i + length;
      let best = 0;
      for (let k = i + 1; k < j; k++) {
        const value = dp[i][k] + dp[k][j] + a[i] * a[k] * a[j];
        if (value > best) best = value;
      }
      dp[i][j] = best;
    }
  }
  return dp[0][n - 1];
}

console.log(maxCoins([3, 1, 5, 8]));
