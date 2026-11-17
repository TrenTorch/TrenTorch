// O(n log n) time, O(n) space
class MaxHeap {
  constructor() {
    this.data = [];
  }
  size() {
    return this.data.length;
  }
  push(val) {
    this.data.push(val);
    this._siftUp(this.data.length - 1);
  }
  _siftUp(idx) {
    while (idx > 0) {
      const parent = (idx - 1) >> 1;
      if (this.data[parent] >= this.data[idx]) break;
      [this.data[parent], this.data[idx]] = [this.data[idx], this.data[parent]];
      idx = parent;
    }
  }
  pop() {
    if (this.data.length === 0) return undefined;
    const top = this.data[0];
    const last = this.data.pop();
    if (this.data.length > 0) {
      this.data[0] = last;
      this._siftDown(0);
    }
    return top;
  }
  _siftDown(idx) {
    const n = this.data.length;
    while (true) {
      let left = idx * 2 + 1;
      let right = left + 1;
      let largest = idx;
      if (left < n && this.data[left] > this.data[largest]) largest = left;
      if (right < n && this.data[right] > this.data[largest]) largest = right;
      if (largest === idx) break;
      [this.data[idx], this.data[largest]] = [this.data[largest], this.data[idx]];
      idx = largest;
    }
  }
}

function findMaximizedCapital(k, w, profits, capital) {
  const projects = capital.map((c, i) => ({ capital: c, profit: profits[i] }));
  projects.sort((a, b) => a.capital - b.capital);
  const heap = new MaxHeap();
  let i = 0;
  for (let cnt = 0; cnt < k; cnt++) {
    while (i < projects.length && projects[i].capital <= w) {
      heap.push(projects[i].profit);
      i++;
    }
    if (heap.size() === 0) break;
    w += heap.pop();
  }
  return w;
}

console.log(findMaximizedCapital(2, 0, [1, 2, 3], [0, 1, 1]));
