// O(n log n) time, O(n) space
function lastStoneWeight(stones) {
  class MaxHeap {
    constructor(arr = []) {
      this.heap = arr;
      this.heapify();
    }
    heapify() {
      for (let i = Math.floor(this.heap.length / 2) - 1; i >= 0; i--) {
        this.siftDown(i);
      }
    }
    push(val) {
      this.heap.push(val);
      this.siftUp(this.heap.length - 1);
    }
    pop() {
      if (this.heap.length === 0) return undefined;
      const max = this.heap[0];
      const end = this.heap.pop();
      if (this.heap.length > 0) {
        this.heap[0] = end;
        this.siftDown(0);
      }
      return max;
    }
    size() {
      return this.heap.length;
    }
    peek() {
      return this.heap[0];
    }
    siftUp(i) {
      while (i > 0) {
        const parent = Math.floor((i - 1) / 2);
        if (this.heap[parent] >= this.heap[i]) break;
        [this.heap[parent], this.heap[i]] = [this.heap[i], this.heap[parent]];
        i = parent;
      }
    }
    siftDown(i) {
      const length = this.heap.length;
      while (true) {
        let largest = i;
        const left = 2 * i + 1;
        const right = 2 * i + 2;
        if (left < length && this.heap[left] > this.heap[largest]) largest = left;
        if (right < length && this.heap[right] > this.heap[largest]) largest = right;
        if (largest === i) break;
        [this.heap[i], this.heap[largest]] = [this.heap[largest], this.heap[i]];
        i = largest;
      }
    }
  }

  const heap = new MaxHeap(stones);
  while (heap.size() > 1) {
    const a = heap.pop();
    const b = heap.pop();
    if (a !== b) {
      heap.push(a - b);
    }
  }
  return heap.size() === 1 ? heap.peek() : 0;
}

console.log(lastStoneWeight([2, 7, 4, 1, 8, 1]));
