// O(n + m) time, O(n + m) space
function isBipartite(n, edges) {
  const adj = new Array(n).fill(null).map(() => []);
  for (const [a, b] of edges) {
    adj[a].push(b);
    adj[b].push(a);
  }
  const color = new Array(n).fill(-1);
  for (let start = 0; start < n; start++) {
    if (color[start] !== -1) continue;
    color[start] = 0;
    const queue = [start];
    let qIndex = 0;
    while (qIndex < queue.length) {
      const node = queue[qIndex++];
      for (const nxt of adj[node]) {
        if (color[nxt] === -1) {
          color[nxt] = 1 - color[node];
          queue.push(nxt);
        } else if (color[nxt] === color[node]) {
          return false;
        }
      }
    }
  }
  return true;
}

console.log(isBipartite(4, [[0, 1], [1, 2], [2, 3], [3, 0]]));
