// O(N log k) time, O(k) space where N is total elements, k is number of arrays
function mergeKArrays(arrays) {
  // Min-heap implementation
  const heap = [];
  
  function push(item) {
    heap.push(item);
    let idx = heap.length - 1;
    while (idx > 0) {
      const parentIdx = Math.floor((idx - 1) / 2);
      if (heap[parentIdx][0] <= heap[idx][0]) break;
      [heap[parentIdx], heap[idx]] = [heap[idx], heap[parentIdx]];
      idx = parentIdx;
    }
  }
  
  function pop() {
    if (heap.length === 0) return null;
    const min = heap[0];
    const end = heap.pop();
    if (heap.length > 0) {
      heap[0] = end;
      let idx = 0;
      const length = heap.length;
      while (true) {
        const leftIdx = 2 * idx + 1;
        const rightIdx = 2 * idx + 2;
        let smallest = idx;
        if (leftIdx < length && heap[leftIdx][0] < heap[smallest][0]) {
          smallest = leftIdx;
        }
        if (rightIdx < length && heap[rightIdx][0] < heap[smallest][0]) {
          smallest = rightIdx;
        }
        if (smallest === idx) break;
        [heap[idx], heap[smallest]] = [heap[smallest], heap[idx]];
        idx = smallest;
      }
    }
    return min;
  }
  
  // Initialize heap with first element of each non-empty array
  for (let i = 0; i < arrays.length; i++) {
    if (arrays[i].length > 0) {
      push([arrays[i][0], i, 0]);
    }
  }
  
  const out = [];
  while (heap.length > 0) {
    const [value, i, j] = pop();
    out.push(value);
    if (j + 1 < arrays[i].length) {
      push([arrays[i][j + 1], i, j + 1]);
    }
  }
  
  return out;
}

console.log(mergeKArrays([[1, 4, 5], [1, 3, 4], [2, 6]]));
