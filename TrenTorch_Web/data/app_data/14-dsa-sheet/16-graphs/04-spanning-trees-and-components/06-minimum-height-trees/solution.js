// O(n) time, O(n) space
function minHeightTrees(n, edges) {
  if (n <= 2) {
    return Array.from({length: n}, (_, i) => i);
  }
  const adj = Array.from({length: n}, () => []);
  for (const [a, b] of edges) {
    adj[a].push(b);
    adj[b].push(a);
  }
  const degree = adj.map(neighbors => neighbors.length);
  let leaves = [];
  for (let i = 0; i < n; i++) {
    if (degree[i] === 1) leaves.push(i);
  }
  let remaining = n;
  while (remaining > 2) {
    remaining -= leaves.length;
    const nxt = [];
    for (const leaf of leaves) {
      for (const other of adj[leaf]) {
        degree[other]--;
        if (degree[other] === 1) {
          nxt.push(other);
        }
      }
    }
    leaves = nxt;
  }
  leaves.sort((a, b) => a - b);
  return leaves;
}

console.log(minHeightTrees(6, [[3, 0], [3, 1], [3, 2], [3, 4], [5, 4]]));
