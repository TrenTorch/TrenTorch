// O(n^3) time, O(n^2) space
function allPairsShortest(n, edges) {
  const INF = Infinity;
  const dist = Array.from({ length: n }, () => Array(n).fill(INF));
  for (let i = 0; i < n; i++) dist[i][i] = 0;
  for (const [a, b, w] of edges) {
    if (w < dist[a][b]) dist[a][b] = w;
  }
  for (let k = 0; k < n; k++) {
    const rowK = dist[k];
    for (let i = 0; i < n; i++) {
      const dik = dist[i][k];
      if (dik === INF) continue;
      const rowI = dist[i];
      for (let j = 0; j < n; j++) {
        const alt = dik + rowK[j];
        if (alt < rowI[j]) rowI[j] = alt;
      }
    }
  }
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      if (dist[i][j] === INF) dist[i][j] = -1;
    }
  }
  return dist;
}

console.log(allPairsShortest(3, [[0, 1, 4], [1, 2, 1], [0, 2, 7]]));
