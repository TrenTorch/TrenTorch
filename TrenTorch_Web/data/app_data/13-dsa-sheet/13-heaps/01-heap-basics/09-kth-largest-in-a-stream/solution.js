// O((n+m) log k) time, O(k) space
function kthLargestStream(k, nums, adds) {
  class MinHeap {
    constructor() {
      this.heap = [];
    }
    size() {
      return this.heap.length;
    }
    peek() {
      return this.heap[0];
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
    pushPop(val) {
      if (this.heap.length === 0 || val <= this.heap[0]) {
        return val;
      }
      const top = this.heap[0];
      this.heap[0] = val;
      this._siftDown(0);
      return top;
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

  const heap = new MinHeap();
  for (const x of nums) {
    heap.push(x);
    if (heap.size() > k) heap.pop();
  }
  const out = [];
  for (const x of adds) {
    if (heap.size() < k) {
      heap.push(x);
    } else {
      heap.pushPop(x);
    }
    out.push(heap.peek());
  }
  return out;
}

console.log(kthLargestStream(3, [4, 5, 8, 2], [3, 5, 10, 9, 4]));
