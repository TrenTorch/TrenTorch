// O(n^2 * 2^n) time, O(n * 2^n) space
function tsp(dist) {
  const n = dist.length;
  if (n <= 1) return 0;
  const INF = Infinity;
  const full = (1 << n) - 1;
  const best = Array.from({ length: 1 << n }, () => Array(n).fill(INF));
  best[1][0] = 0;
  for (let mask = 1; mask <= full; mask++) {
    if ((mask & 1) === 0) continue;
    for (let last = 0; last < n; last++) {
      const cost = best[mask][last];
      if (cost === INF) continue;
      for (let nxt = 0; nxt < n; nxt++) {
        if ((mask >> nxt) & 1) continue;
        const newMask = mask | (1 << nxt);
        const value = cost + dist[last][nxt];
        if (value < best[newMask][nxt]) {
          best[newMask][nxt] = value;
        }
      }
    }
  }
  let ans = INF;
  for (let last = 1; last < n; last++) {
    const total = best[full][last] + dist[last][0];
    if (total < ans) ans = total;
  }
  return ans;
}

console.log(tsp([[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]));
