// O((n + m) log n) time, O(n + m) space
function shortestDistances(n, edges, source) {
  const adj = Array.from({ length: n }, () => []);
  for (const [a, b, w] of edges) {
    adj[a].push([b, w]);
  }
  const INF = Infinity;
  const dist = Array(n).fill(INF);
  dist[source] = 0;

  // Min-heap implementation
  const heap = [];
  function push(item) {
    heap.push(item);
    let i = heap.length - 1;
    while (i > 0) {
      const p = (i - 1) >> 1;
      if (heap[p][0] <= heap[i][0]) break;
      [heap[p], heap[i]] = [heap[i], heap[p]];
      i = p;
    }
  }
  function pop() {
    const top = heap[0];
    const end = heap.pop();
    if (heap.length > 0) {
      heap[0] = end;
      let i = 0;
      const len = heap.length;
      while (true) {
        const left = (i << 1) + 1;
        const right = left + 1;
        let smallest = i;
        if (left < len && heap[left][0] < heap[smallest][0]) smallest = left;
        if (right < len && heap[right][0] < heap[smallest][0]) smallest = right;
        if (smallest === i) break;
        [heap[i], heap[smallest]] = [heap[smallest], heap[i]];
        i = smallest;
      }
    }
    return top;
  }

  push([0, source]);
  while (heap.length) {
    const [d, u] = pop();
    if (d > dist[u]) continue;
    for (const [v, w] of adj[u]) {
      const nd = d + w;
      if (nd < dist[v]) {
        dist[v] = nd;
        push([nd, v]);
      }
    }
  }
  return dist.map(d => (d === INF ? -1 : d));
}

console.log(shortestDistances(3, [[0, 1, 4], [0, 2, 1], [2, 1, 2]], 0));
