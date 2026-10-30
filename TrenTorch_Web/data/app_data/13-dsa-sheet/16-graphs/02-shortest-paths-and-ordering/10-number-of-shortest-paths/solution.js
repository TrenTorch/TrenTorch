// O((n + m) log n) time, O(n + m) space
function countShortestPaths(n, roads) {
  const MOD = 1000000007;
  if (n === 1) return 1;

  const adj = Array.from({ length: n }, () => []);
  for (const [a, b, t] of roads) {
    adj[a].push([b, t]);
    adj[b].push([a, t]);
  }

  const dist = new Array(n).fill(Infinity);
  const ways = new Array(n).fill(0);
  dist[0] = 0;
  ways[0] = 1;

  const heap = new MinHeap();
  heap.push([0, 0]); // [distance, node]

  while (!heap.isEmpty()) {
    const [d, u] = heap.pop();
    if (d > dist[u]) continue;

    for (const [v, t] of adj[u]) {
      const nd = d + t;
      if (nd < dist[v]) {
        dist[v] = nd;
        ways[v] = ways[u];
        heap.push([nd, v]);
      } else if (nd === dist[v]) {
        ways[v] = (ways[v] + ways[u]) % MOD;
      }
    }
  }

  return ways[n - 1] % MOD;
}

class MinHeap {
  constructor() {
    this.heap = [];
  }
  isEmpty() {
    return this.heap.length === 0;
  }
  push(item) {
    this.heap.push(item);
    this._siftUp(this.heap.length - 1);
  }
  pop() {
    const top = this.heap[0];
    const end = this.heap.pop();
    if (this.heap.length > 0) {
      this.heap[0] = end;
      this._siftDown(0);
    }
    return top;
  }
  _siftUp(idx) {
    while (idx > 0) {
      const parent = (idx - 1) >> 1;
      if (this.heap[parent][0] <= this.heap[idx][0]) break;
      [this.heap[parent], this.heap[idx]] = [this.heap[idx], this.heap[parent]];
      idx = parent;
    }
  }
  _siftDown(idx) {
    const length = this.heap.length;
    while (true) {
      let left = idx * 2 + 1;
      let right = idx * 2 + 2;
      let smallest = idx;

      if (left < length && this.heap[left][0] < this.heap[smallest][0]) {
        smallest = left;
      }
      if (right < length && this.heap[right][0] < this.heap[smallest][0]) {
        smallest = right;
      }
      if (smallest === idx) break;
      [this.heap[smallest], this.heap[idx]] = [this.heap[idx], this.heap[smallest]];
      idx = smallest;
    }
  }
}

console.log(countShortestPaths(4, [[0, 1, 1], [0, 2, 1], [1, 3, 1], [2, 3, 1]]));
