class MinHeap {
  constructor() {
    this.heap = [];
  }
  push(item) {
    this.heap.push(item);
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
  peek() {
    return this.heap[0];
  }
  size() {
    return this.heap.length;
  }
  _bubbleUp(idx) {
    while (idx > 0) {
      const parentIdx = Math.floor((idx - 1) / 2);
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

// O(N log k) time, O(k) space where N is total number of elements, k is number of lists
function smallestRange(lists) {
  const heap = new MinHeap();
  let currentMax = -Infinity;
  for (let i = 0; i < lists.length; i++) {
    const val = lists[i][0];
    heap.push([val, i, 0]);
    if (val > currentMax) currentMax = val;
  }
  let bestLo = heap.peek()[0];
  let bestHi = currentMax;
  while (true) {
    const [value, i, j] = heap.pop();
    const currentRange = currentMax - value;
    const bestRange = bestHi - bestLo;
    if (currentRange < bestRange || (currentRange === bestRange && value < bestLo)) {
      bestLo = value;
      bestHi = currentMax;
    }
    if (j + 1 === lists[i].length) {
      return [bestLo, bestHi];
    }
    const nxt = lists[i][j + 1];
    if (nxt > currentMax) currentMax = nxt;
    heap.push([nxt, i, j + 1]);
  }
}

console.log(smallestRange([[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]]));
