// O(colors^n) time, O(n + e) space
function canColorGraph(n, edges, colors) {
  // Check for self-loops
  for (const [u, v] of edges) {
    if (u === v) return false;
  }

  // Build adjacency list
  const adj = Array.from({ length: n }, () => []);
  for (const [u, v] of edges) {
    adj[u].push(v);
    adj[v].push(u);
  }

  const color = new Array(n).fill(-1);

  function go(i) {
    if (i === n) return true;
    for (let c = 0; c < colors; c++) {
      let ok = true;
      for (const j of adj[i]) {
        if (color[j] === c) {
          ok = false;
          break;
        }
      }
      if (ok) {
        color[i] = c;
        if (go(i + 1)) return true;
        color[i] = -1;
      }
    }
    return false;
  }

  return go(0);
}

console.log(canColorGraph(3, [[0, 1], [1, 2], [0, 2]], 3));
