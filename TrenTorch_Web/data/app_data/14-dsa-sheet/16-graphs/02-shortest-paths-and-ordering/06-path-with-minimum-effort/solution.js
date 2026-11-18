// O(m * n * log(m * n)) time, O(m * n) space where m = rows, n = cols
class MinHeap {
  constructor() {
    this.heap = [];
  }
  push(val) {
    this.heap.push(val);
    this._bubbleUp(this.heap.length - 1);
  }
  pop() {
    if (this.heap.length === 0) return null;
    const top = this.heap[0];
    const end = this.heap.pop();
    if (this.heap.length > 0) {
      this.heap[0] = end;
      this._bubbleDown(0);
    }
    return top;
  }
  size() {
    return this.heap.length;
  }
  _bubbleUp(idx) {
    while (idx > 0) {
      const parentIdx = (idx - 1) >> 1;
      if (this.heap[parentIdx][0] <= this.heap[idx][0]) break;
      [this.heap[parentIdx], this.heap[idx]] = [this.heap[idx], this.heap[parentIdx]];
      idx = parentIdx;
    }
  }
  _bubbleDown(idx) {
    const length = this.heap.length;
    while (true) {
      let smallest = idx;
      const left = 2 * idx + 1;
      const right = 2 * idx + 2;
      if (left < length && this.heap[left][0] < this.heap[smallest][0]) smallest = left;
      if (right < length && this.heap[right][0] < this.heap[smallest][0]) smallest = right;
      if (smallest === idx) break;
      [this.heap[idx], this.heap[smallest]] = [this.heap[smallest], this.heap[idx]];
      idx = smallest;
    }
  }
}

function minimumEffortPath(heights) {
  const rows = heights.length;
  const cols = heights[0].length;
  const effort = Array.from({ length: rows }, () => Array(cols).fill(Infinity));
  effort[0][0] = 0;
  const heap = new MinHeap();
  heap.push([0, 0, 0]);
  const dirs = [[1, 0], [-1, 0], [0, 1], [0, -1]];
  while (heap.size() > 0) {
    const [e, x, y] = heap.pop();
    if (x === rows - 1 && y === cols - 1) return e;
    if (e > effort[x][y]) continue;
    for (const [dx, dy] of dirs) {
      const nx = x + dx;
      const ny = y + dy;
      if (nx >= 0 && nx < rows && ny >= 0 && ny < cols) {
        const ne = Math.max(e, Math.abs(heights[nx][ny] - heights[x][y]));
        if (ne < effort[nx][ny]) {
          effort[nx][ny] = ne;
          heap.push([ne, nx, ny]);
        }
      }
    }
  }
  return 0;
}

console.log(minimumEffortPath([[1, 2, 2], [3, 8, 2], [5, 3, 5]]));
