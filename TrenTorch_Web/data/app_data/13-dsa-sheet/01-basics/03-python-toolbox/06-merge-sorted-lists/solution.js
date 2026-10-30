// O(N log k) time, O(k) space where N is total elements and k is number of lists
function mergeSortedLists(lists) {
  const heap = [];
  const result = [];

  // Initialize heap with first element from each non-empty list
  for (let i = 0; i < lists.length; i++) {
    if (lists[i].length > 0) {
      heap.push({ val: lists[i][0], listIdx: i, elemIdx: 0 });
    }
  }

  // Build min-heap
  function heapify(arr, n, i) {
    let smallest = i;
    const left = 2 * i + 1;
    const right = 2 * i + 2;

    if (left < n && arr[left].val < arr[smallest].val) {
      smallest = left;
    }
    if (right < n && arr[right].val < arr[smallest].val) {
      smallest = right;
    }
    if (smallest !== i) {
      [arr[i], arr[smallest]] = [arr[smallest], arr[i]];
      heapify(arr, n, smallest);
    }
  }

  function buildHeap(arr) {
    const n = arr.length;
    for (let i = Math.floor(n / 2) - 1; i >= 0; i--) {
      heapify(arr, n, i);
    }
  }

  function heappop(arr) {
    const min = arr[0];
    const end = arr.pop();
    if (arr.length > 0) {
      arr[0] = end;
      heapify(arr, arr.length, 0);
    }
    return min;
  }

  function heappush(arr, item) {
    arr.push(item);
    let i = arr.length - 1;
    while (i > 0) {
      const parent = Math.floor((i - 1) / 2);
      if (arr[i].val >= arr[parent].val) break;
      [arr[i], arr[parent]] = [arr[parent], arr[i]];
      i = parent;
    }
  }

  buildHeap(heap);

  while (heap.length > 0) {
    const { val, listIdx, elemIdx } = heappop(heap);
    result.push(val);

    const nextElemIdx = elemIdx + 1;
    if (nextElemIdx < lists[listIdx].length) {
      heappush(heap, {
        val: lists[listIdx][nextElemIdx],
        listIdx: listIdx,
        elemIdx: nextElemIdx
      });
    }
  }

  return result;
}

console.log(mergeSortedLists([[1, 4, 7], [2, 5], [3, 6, 9]]));
