// O(n + m) time, O(n + m) space where m = edges.length
function countComponents(n, edges) {
  const adj = Array.from({ length: n }, () => []);
  for (const [a, b] of edges) {
    adj[a].push(b);
    adj[b].push(a);
  }
  const seen = new Array(n).fill(false);
  let count = 0;
  for (let start = 0; start < n; start++) {
    if (seen[start]) continue;
    count++;
    seen[start] = true;
    const stack = [start];
    while (stack.length) {
      const node = stack.pop();
      for (const nxt of adj[node]) {
        if (!seen[nxt]) {
          seen[nxt] = true;
          stack.push(nxt);
        }
      }
    }
  }
  return count;
}

console.log(countComponents(5, [[0, 1], [1, 2], [3, 4]]));
