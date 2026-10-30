// O(n + m) time, O(n + m) space
function criticalConnections(n, connections) {
  const adj = Array.from({ length: n }, () => []);
  for (const [a, b] of connections) {
    adj[a].push(b);
    adj[b].push(a);
  }
  const disc = new Array(n).fill(-1);
  const low = new Array(n).fill(0);
  const bridges = [];
  let timer = 0;

  for (let root = 0; root < n; root++) {
    if (disc[root] !== -1) continue;
    disc[root] = low[root] = timer++;
    const stack = [[root, -1, 0]];
    while (stack.length) {
      const [node, parent, i] = stack.pop();
      if (i < adj[node].length) {
        stack.push([node, parent, i + 1]);
        const nxt = adj[node][i];
        if (nxt === parent) continue;
        if (disc[nxt] === -1) {
          disc[nxt] = low[nxt] = timer++;
          stack.push([nxt, node, 0]);
        } else {
          low[node] = Math.min(low[node], disc[nxt]);
        }
      } else if (parent !== -1) {
        low[parent] = Math.min(low[parent], low[node]);
        if (low[node] > disc[parent]) {
          bridges.push([Math.min(parent, node), Math.max(parent, node)]);
        }
      }
    }
  }

  bridges.sort((a, b) => (a[0] - b[0]) || (a[1] - b[1]));
  return bridges;
}

console.log(criticalConnections(4, [[0, 1], [1, 2], [2, 0], [1, 3]]));
