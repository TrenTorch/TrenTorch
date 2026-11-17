// O(n + m) time, O(n + m) space
function eventualSafeNodes(n, edges) {
  const rev = Array.from({ length: n }, () => []);
  const outDegree = new Array(n).fill(0);
  for (const [a, b] of edges) {
    rev[b].push(a);
    outDegree[a]++;
  }
  const queue = [];
  for (let v = 0; v < n; v++) {
    if (outDegree[v] === 0) queue.push(v);
  }
  const safe = new Array(n).fill(false);
  let head = 0;
  while (head < queue.length) {
    const node = queue[head++];
    safe[node] = true;
    for (const p of rev[node]) {
      outDegree[p]--;
      if (outDegree[p] === 0) queue.push(p);
    }
  }
  const result = [];
  for (let v = 0; v < n; v++) {
    if (safe[v]) result.push(v);
  }
  return result;
}

console.log(eventualSafeNodes(7, [[0, 1], [0, 2], [1, 2], [1, 3], [2, 5], [3, 0], [4, 5]]));
