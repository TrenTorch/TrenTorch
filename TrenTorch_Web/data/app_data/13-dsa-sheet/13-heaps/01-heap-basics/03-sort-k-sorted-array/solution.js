function sortKSorted(nums, k) {
  // O(n log k) time, O(k) space
  if (nums.length === 0) return [];
  
  // Min-heap implementation using array
  const heap = [];
  
  function heapify(arr) {
    const n = arr.length;
    for (let i = Math.floor(n / 2) - 1; i >= 0; i--) {
      siftDown(arr, i, n);
    }
  }
  
  function siftDown(arr, i, n) {
    while (true) {
      let smallest = i;
      const left = 2 * i + 1;
      const right = 2 * i + 2;
      if (left < n && arr[left] < arr[smallest]) smallest = left;
      if (right < n && arr[right] < arr[smallest]) smallest = right;
      if (smallest === i) break;
      [arr[i], arr[smallest]] = [arr[smallest], arr[i]];
      i = smallest;
    }
  }
  
  function heappush(arr, val) {
    arr.push(val);
    let i = arr.length - 1;
    while (i > 0) {
      const parent = Math.floor((i - 1) / 2);
      if (arr[parent] <= arr[i]) break;
      [arr[i], arr[parent]] = [arr[parent], arr[i]];
      i = parent;
    }
  }
  
  function heappop(arr) {
    const min = arr[0];
    const end = arr.pop();
    if (arr.length > 0) {
      arr[0] = end;
      siftDown(arr, 0, arr.length);
    }
    return min;
  }
  
  function heappushpop(arr, val) {
    if (arr.length > 0 && val > arr[0]) {
      const min = arr[0];
      arr[0] = val;
      siftDown(arr, 0, arr.length);
      return min;
    }
    return val;
  }
  
  // Initialize heap with first k+1 elements
  const initialSize = Math.min(k + 1, nums.length);
  for (let i = 0; i < initialSize; i++) {
    heap.push(nums[i]);
  }
  heapify(heap);
  
  const out = [];
  // Process remaining elements
  for (let i = k + 1; i < nums.length; i++) {
    out.push(heappushpop(heap, nums[i]));
  }
  // Extract remaining elements from heap
  while (heap.length > 0) {
    out.push(heappop(heap));
  }
  return out;
}

console.log(sortKSorted([6, 5, 3, 2, 8, 10, 9], 3));
