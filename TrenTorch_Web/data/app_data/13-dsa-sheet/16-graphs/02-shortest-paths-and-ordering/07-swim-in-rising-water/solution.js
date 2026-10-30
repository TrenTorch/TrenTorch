// O(N log N) time, O(N) space where N = rows * cols

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
    const min = this.heap[0];
    const end = this.heap.pop();
    if (this.heap.length > 0) {
      this.heap[0] = end;
      this._bubbleDown(0);
    }
    return min;
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
      if (left < length && this.heap[left][0] < this.heap[smallest][0]) {
        smallest = left;
      }
      if (right < length && this.heap[right][0] < this.heap[smallest][0]) {
        smallest = right;
      }
      if (smallest === idx) break;
      [this.heap[idx], this.heap[smallest]] = [this.heap[smallest], this.heap[idx]];
      idx = smallest;
    }
  }
}

function swimInWater(grid) {
  const n = grid.length;
  const m = grid[0].length;
  const seen = Array.from({ length: n }, () => Array(m).fill(false));
  const heap = new MinHeap();
  heap.push([grid[0][0], 0, 0]);
  seen[0][0] = true;
  const dirs = [[1, 0], [-1, 0], [0, 1], [0, -1]];
  while (heap.size() > 0) {
    const [t, x, y] = heap.pop();
    if (x === n - 1 && y === m - 1) {
      return t;
    }
    for (const [dx, dy] of dirs) {
      const nx = x + dx;
      const ny = y + dy;
      if (nx >= 0 && nx < n && ny >= 0 && ny < m && !seen[nx][ny]) {
        seen[nx][ny] = true;
        heap.push([Math.max(t, grid[nx][ny]), nx, ny]);
      }
    }
  }
  return 0;
}

console.log(swimInWater([[0, 2], [1, 3]]));
