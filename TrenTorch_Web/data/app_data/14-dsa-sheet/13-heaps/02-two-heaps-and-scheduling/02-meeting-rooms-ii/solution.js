// O(n log n) time, O(n) space
function minMeetingRooms(meetings) {
  // Min-heap implementation
  class MinHeap {
    constructor() {
      this.heap = [];
    }
    peek() {
      return this.heap[0];
    }
    size() {
      return this.heap.length;
    }
    push(val) {
      this.heap.push(val);
      this._bubbleUp(this.heap.length - 1);
    }
    replace(val) {
      // Assumes heap is not empty
      this.heap[0] = val;
      this._bubbleDown(0);
    }
    _bubbleUp(idx) {
      while (idx > 0) {
        const parentIdx = Math.floor((idx - 1) / 2);
        if (this.heap[parentIdx] <= this.heap[idx]) break;
        [this.heap[parentIdx], this.heap[idx]] = [this.heap[idx], this.heap[parentIdx]];
        idx = parentIdx;
      }
    }
    _bubbleDown(idx) {
      const lastIdx = this.heap.length - 1;
      while (true) {
        const leftIdx = 2 * idx + 1;
        const rightIdx = 2 * idx + 2;
        let smallest = idx;
        if (leftIdx <= lastIdx && this.heap[leftIdx] < this.heap[smallest]) {
          smallest = leftIdx;
        }
        if (rightIdx <= lastIdx && this.heap[rightIdx] < this.heap[smallest]) {
          smallest = rightIdx;
        }
        if (smallest === idx) break;
        [this.heap[idx], this.heap[smallest]] = [this.heap[smallest], this.heap[idx]];
        idx = smallest;
      }
    }
  }

  const rooms = new MinHeap();
  // Sort meetings by start time
  meetings.sort((a, b) => a[0] - b[0]);
  for (const [start, end] of meetings) {
    if (rooms.size() > 0 && rooms.peek() <= start) {
      rooms.replace(end);
    } else {
      rooms.push(end);
    }
  }
  return rooms.size();
}

console.log(minMeetingRooms([[0, 30], [5, 10], [15, 20]]));
