class MinHeap {
  constructor() {
    this.data = [];
  }
  push(val) {
    this.data.push(val);
    this.bubbleUp(this.data.length - 1);
  }
  pop() {
    const min = this.data[0];
    const end = this.data.pop();
    if (this.data.length > 0) {
      this.data[0] = end;
      this.bubbleDown(0);
    }
    return min;
  }
  peek() {
    return this.data[0];
  }
  size() {
    return this.data.length;
  }
  isEmpty() {
    return this.data.length === 0;
  }
  bubbleUp(i) {
    while (i > 0) {
      const parent = (i - 1) >> 1;
      if (this.data[parent] <= this.data[i]) break;
      [this.data[parent], this.data[i]] = [this.data[i], this.data[parent]];
      i = parent;
    }
  }
  bubbleDown(i) {
    const length = this.data.length;
    while (true) {
      let smallest = i;
      const left = 2 * i + 1;
      const right = 2 * i + 2;
      if (left < length && this.data[left] < this.data[smallest]) smallest = left;
      if (right < length && this.data[right] < this.data[smallest]) smallest = right;
      if (smallest === i) break;
      [this.data[i], this.data[smallest]] = [this.data[smallest], this.data[i]];
      i = smallest;
    }
  }
}

// O(n log k) time, O(k) space
function medianSlidingWindow(nums, k) {
  const small = new MinHeap(); // max-heap via negatives
  const large = new MinHeap(); // min-heap
  const delayed = new Map();
  let sizeSmall = 0;
  let sizeLarge = 0;

  function clean(heap, isSmall) {
    while (!heap.isEmpty()) {
      const val = isSmall ? -heap.peek() : heap.peek();
      const count = delayed.get(val) || 0;
      if (count > 0) {
        delayed.set(val, count - 1);
        heap.pop();
      } else {
        break;
      }
    }
  }

  function balance() {
    if (sizeSmall > sizeLarge + 1) {
      const val = -small.pop();
      large.push(val);
      sizeSmall--;
      sizeLarge++;
      clean(small, true);
    } else if (sizeSmall < sizeLarge) {
      const val = large.pop();
      small.push(-val);
      sizeLarge--;
      sizeSmall++;
      clean(large, false);
    }
  }

  function add(x) {
    if (small.isEmpty() || x <= -small.peek()) {
      small.push(-x);
      sizeSmall++;
    } else {
      large.push(x);
      sizeLarge++;
    }
    balance();
  }

  function remove(x) {
    delayed.set(x, (delayed.get(x) || 0) + 1);
    if (x <= -small.peek()) {
      sizeSmall--;
      if (x === -small.peek()) {
        clean(small, true);
      }
    } else {
      sizeLarge--;
      if (x === large.peek()) {
        clean(large, false);
      }
    }
    balance();
  }

  function median() {
    if (k % 2 === 1) {
      return -small.peek();
    }
    return (-small.peek() + large.peek()) / 2;
  }

  for (const x of nums.slice(0, k)) {
    add(x);
  }
  const out = [median()];
  for (let i = k; i < nums.length; i++) {
    add(nums[i]);
    remove(nums[i - k]);
    out.push(median());
  }
  return out;
}

console.log(medianSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3));
