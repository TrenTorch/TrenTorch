// O(n log n) time, O(n) space
function connectRopes(ropes) {
  const heap = [...ropes];
  // heapify
  for (let i = Math.floor(heap.length / 2) - 1; i >= 0; i--) {
    heapifyDown(heap, i);
  }

  function heapifyDown(arr, i) {
    const n = arr.length;
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

  function heapPush(arr, val) {
    arr.push(val);
    let i = arr.length - 1;
    while (i > 0) {
      const parent = Math.floor((i - 1) / 2);
      if (arr[parent] <= arr[i]) break;
      [arr[i], arr[parent]] = [arr[parent], arr[i]];
      i = parent;
    }
  }

  function heapPop(arr) {
    if (arr.length === 0) return undefined;
    const top = arr[0];
    const end = arr.pop();
    if (arr.length > 0) {
      arr[0] = end;
      heapifyDown(arr, 0);
    }
    return top;
  }

  let total = 0;
  while (heap.length > 1) {
    const a = heapPop(heap);
    const b = heapPop(heap);
    const joined = a + b;
    total += joined;
    heapPush(heap, joined);
  }
  return total;
}

console.log(connectRopes([4, 3, 2, 6]));
