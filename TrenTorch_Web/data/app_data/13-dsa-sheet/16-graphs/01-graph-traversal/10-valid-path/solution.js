// O(n + e) time, O(n + e) space
function validPath(n, edges, source, destination) {
  const adj = new Array(n).fill(null).map(() => []);
  for (const [a, b] of edges) {
    adj[a].push(b);
    adj[b].push(a);
  }
  const seen = new Array(n).fill(false);
  seen[source] = true;
  const stack = [source];
  while (stack.length > 0) {
    const node = stack.pop();
    if (node === destination) return true;
    for (const nxt of adj[node]) {
      if (!seen[nxt]) {
        seen[nxt] = true;
        stack.push(nxt);
      }
    }
  }
  return false;
}

console.log(validPath(3, [[0, 1], [1, 2], [2, 0]], 0, 2));
