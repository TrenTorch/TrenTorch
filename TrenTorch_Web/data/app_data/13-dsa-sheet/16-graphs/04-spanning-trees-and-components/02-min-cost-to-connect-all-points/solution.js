// O(n^2) time, O(n) space
function minCostConnectPoints(points) {
  const n = points.length;
  if (n === 0) return 0;
  const INF = Number.POSITIVE_INFINITY;
  const best = new Array(n).fill(INF);
  best[0] = 0;
  const used = new Array(n).fill(false);
  let total = 0;
  for (let i = 0; i < n; i++) {
    let u = -1;
    for (let v = 0; v < n; v++) {
      if (!used[v] && (u === -1 || best[v] < best[u])) {
        u = v;
      }
    }
    used[u] = true;
    total += best[u];
    const [ux, uy] = points[u];
    for (let v = 0; v < n; v++) {
      if (!used[v]) {
        const dist = Math.abs(points[v][0] - ux) + Math.abs(points[v][1] - uy);
        if (dist < best[v]) {
          best[v] = dist;
        }
      }
    }
  }
  return total;
}

console.log(minCostConnectPoints([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]));
