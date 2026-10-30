// O(n + m) time, O(n + m) space where n is number of nodes, m is number of edges
function hasCycleDirected(n, edges) {
  const adj = Array.from({ length: n }, () => []);
  for (const [a, b] of edges) {
    adj[a].push(b);
  }
  const state = new Array(n).fill(0);
  for (let start = 0; start < n; start++) {
    if (state[start] !== 0) continue;
    state[start] = 1;
    const stack = [[start, 0]];
    while (stack.length > 0) {
      const [node, i] = stack.pop();
      if (i < adj[node].length) {
        stack.push([node, i + 1]);
        const nxt = adj[node][i];
        if (state[nxt] === 1) {
          return true;
        }
        if (state[nxt] === 0) {
          state[nxt] = 1;
          stack.push([nxt, 0]);
        }
      } else {
        state[node] = 2;
      }
    }
  }
  return false;
}

console.log(hasCycleDirected(3, [[0, 1], [1, 2], [2, 0]]));
