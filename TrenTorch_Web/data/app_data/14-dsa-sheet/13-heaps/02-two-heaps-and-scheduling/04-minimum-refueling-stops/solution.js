// O(n log n) time, O(n) space
function minRefuelStops(target, startFuel, stations) {
  class MaxHeap {
    constructor() {
      this.heap = [];
    }
    push(val) {
      this.heap.push(val);
      this._bubbleUp(this.heap.length - 1);
    }
    pop() {
      if (this.heap.length === 0) return null;
      const max = this.heap[0];
      const end = this.heap.pop();
      if (this.heap.length > 0) {
        this.heap[0] = end;
        this._bubbleDown(0);
      }
      return max;
    }
    isEmpty() {
      return this.heap.length === 0;
    }
    _bubbleUp(idx) {
      while (idx > 0) {
        const parentIdx = Math.floor((idx - 1) / 2);
        if (this.heap[parentIdx] >= this.heap[idx]) break;
        [this.heap[parentIdx], this.heap[idx]] = [this.heap[idx], this.heap[parentIdx]];
        idx = parentIdx;
      }
    }
    _bubbleDown(idx) {
      const length = this.heap.length;
      while (true) {
        let largest = idx;
        const left = 2 * idx + 1;
        const right = 2 * idx + 2;
        if (left < length && this.heap[left] > this.heap[largest]) largest = left;
        if (right < length && this.heap[right] > this.heap[largest]) largest = right;
        if (largest === idx) break;
        [this.heap[idx], this.heap[largest]] = [this.heap[largest], this.heap[idx]];
        idx = largest;
      }
    }
  }

  const heap = new MaxHeap();
  let reach = startFuel;
  let stops = 0;
  let i = 0;
  while (reach < target) {
    while (i < stations.length && stations[i][0] <= reach) {
      heap.push(stations[i][1]);
      i++;
    }
    if (heap.isEmpty()) return -1;
    reach += heap.pop();
    stops++;
  }
  return stops;
}

console.log(minRefuelStops(100, 10, [[10, 60], [20, 30], [30, 30], [60, 40]]));
