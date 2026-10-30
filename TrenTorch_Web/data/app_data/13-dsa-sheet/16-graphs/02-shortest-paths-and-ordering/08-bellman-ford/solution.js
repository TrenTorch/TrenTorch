// O(n * m) time, O(n) space
function bellmanFord(n, edges, source) {
  const inf = Infinity;
  const dist = new Array(n).fill(inf);
  dist[source] = 0;
  for (let i = 0; i < n - 1; i++) {
    let changed = false;
    for (const [a, b, w] of edges) {
      if (dist[a] !== inf && dist[a] + w < dist[b]) {
        dist[b] = dist[a] + w;
        changed = true;
      }
    }
    if (!changed) break;
  }
  for (const [a, b, w] of edges) {
    if (dist[a] !== inf && dist[a] + w < dist[b]) {
      return [];
    }
  }
  return dist.map(d => d === inf ? null : d);
}

console.log(bellmanFord(3, [[0, 1, 4], [1, 2, -2], [0, 2, 3]], 0));
