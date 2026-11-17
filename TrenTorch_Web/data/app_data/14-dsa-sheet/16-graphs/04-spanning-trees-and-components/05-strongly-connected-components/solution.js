// O(n + m) time, O(n + m) space
function countScc(n, edges) {
  const adj = Array.from({ length: n }, () => []);
  const rev = Array.from({ length: n }, () => []);
  for (const [a, b] of edges) {
    adj[a].push(b);
    rev[b].push(a);
  }
  const seen = new Array(n).fill(false);
  const order = [];
  for (let start = 0; start < n; start++) {
    if (seen[start]) continue;
    seen[start] = true;
    const stack = [[start, 0]];
    while (stack.length > 0) {
      const [node, i] = stack.pop();
      if (i < adj[node].length) {
        stack.push([node, i + 1]);
        const nxt = adj[node][i];
        if (!seen[nxt]) {
          seen[nxt] = true;
          stack.push([nxt, 0]);
        }
      } else {
        order.push(node);
      }
    }
  }
  seen.fill(false);
  let count = 0;
  for (let idx = order.length - 1; idx >= 0; idx--) {
    const start = order[idx];
    if (seen[start]) continue;
    count++;
    seen[start] = true;
    const stack = [start];
    while (stack.length > 0) {
      const node = stack.pop();
      for (const nxt of rev[node]) {
        if (!seen[nxt]) {
          seen[nxt] = true;
          stack.push(nxt);
        }
      }
    }
  }
  return count;
}

console.log(countScc(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]]));
