// O(n log n) time, O(n) space
class MinHeap {
  constructor() {
    this.heap = [];
  }
  push(val) {
    this.heap.push(val);
    this._siftUp(this.heap.length - 1);
  }
  pop() {
    if (this.heap.length === 0) return undefined;
    const top = this.heap[0];
    const end = this.heap.pop();
    if (this.heap.length > 0) {
      this.heap[0] = end;
      this._siftDown(0);
    }
    return top;
  }
  peek() {
    return this.heap[0];
  }
  size() {
    return this.heap.length;
  }
  _siftUp(idx) {
    while (idx > 0) {
      const parentIdx = (idx - 1) >> 1;
      if (this.heap[parentIdx] <= this.heap[idx]) break;
      [this.heap[parentIdx], this.heap[idx]] = [this.heap[idx], this.heap[parentIdx]];
      idx = parentIdx;
    }
  }
  _siftDown(idx) {
    const length = this.heap.length;
    while (true) {
      let smallest = idx;
      const left = 2 * idx + 1;
      const right = 2 * idx + 2;
      if (left < length && this.heap[left] < this.heap[smallest]) smallest = left;
      if (right < length && this.heap[right] < this.heap[smallest]) smallest = right;
      if (smallest === idx) break;
      [this.heap[idx], this.heap[smallest]] = [this.heap[smallest], this.heap[idx]];
      idx = smallest;
    }
  }
}

function runningMedian(nums) {
  const low = new MinHeap(); // max-heap via negatives
  const high = new MinHeap(); // min-heap
  const out = [];
  for (const x of nums) {
    low.push(-x);
    high.push(-low.pop());
    if (high.size() > low.size()) {
      low.push(-high.pop());
    }
    if (low.size() > high.size()) {
      out.push(-low.peek());
    } else {
      out.push((-low.peek() + high.peek()) / 2);
    }
  }
  return out;
}

console.log(runningMedian([5, 15, 1, 3]));
