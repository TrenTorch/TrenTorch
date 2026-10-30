// O(V + E) time, O(V + E) space
function hasCycleUndirected(n, edges) {
  const adj = new Array(n).fill(null).map(() => []);
  for (let i = 0; i < edges.length; i++) {
    const a = edges[i][0];
    const b = edges[i][1];
    if (a === b) {
      return true;
    }
    adj[a].push([b, i]);
    adj[b].push([a, i]);
  }
  const seen = new Array(n).fill(false);
  for (let start = 0; start < n; start++) {
    if (seen[start]) continue;
    seen[start] = true;
    const stack = [[start, -1]];
    while (stack.length > 0) {
      const [node, via] = stack.pop();
      for (const [nxt, edgeId] of adj[node]) {
        if (edgeId === via) continue;
        if (seen[nxt]) {
          return true;
        }
        seen[nxt] = true;
        stack.push([nxt, edgeId]);
      }
    }
  }
  return false;
}

console.log(hasCycleUndirected(4, [[0, 1], [1, 2], [2, 0], [3, 3]]));
