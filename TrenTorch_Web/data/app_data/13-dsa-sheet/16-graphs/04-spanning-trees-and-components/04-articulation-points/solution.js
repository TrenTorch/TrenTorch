function articulationPoints(n, edges) {
  // O(n + m) time, O(n + m) space
  const adj = Array.from({ length: n }, () => []);
  for (const [a, b] of edges) {
    adj[a].push(b);
    adj[b].push(a);
  }
  const disc = new Array(n).fill(-1);
  const low = new Array(n);
  const is_cut = new Array(n).fill(false);
  let timer = 0;
  for (let root = 0; root < n; root++) {
    if (disc[root] !== -1) continue;
    disc[root] = low[root] = timer++;
    let root_children = 0;
    const stack = [[root, -1, 0]];
    while (stack.length > 0) {
      const [node, parent, i] = stack.pop();
      if (i < adj[node].length) {
        stack.push([node, parent, i + 1]);
        const nxt = adj[node][i];
        if (nxt === parent) continue;
        if (disc[nxt] === -1) {
          disc[nxt] = low[nxt] = timer++;
          if (node === root) root_children++;
          stack.push([nxt, node, 0]);
        } else {
          low[node] = Math.min(low[node], disc[nxt]);
        }
      } else if (parent !== -1) {
        low[parent] = Math.min(low[parent], low[node]);
        if (parent !== root && low[node] >= disc[parent]) {
          is_cut[parent] = true;
        }
      }
    }
    if (root_children >= 2) is_cut[root] = true;
  }
  const result = [];
  for (let v = 0; v < n; v++) {
    if (is_cut[v]) result.push(v);
  }
  return result;
}

console.log(articulationPoints(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]]));
