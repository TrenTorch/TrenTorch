class ListNode {
  constructor(val = 0, next = null) {
    this.val = val;
    this.next = next;
  }
}

// O(N log k) time, O(k) space
function mergeKLists(lists) {
  // Min-heap implementation
  const heap = [];

  function heapPush(item) {
    heap.push(item);
    let i = heap.length - 1;
    while (i > 0) {
      const p = (i - 1) >> 1;
      if (heap[p].val < heap[i].val) break;
      if (heap[p].val === heap[i].val && heap[p].idx <= heap[i].idx) break;
      [heap[p], heap[i]] = [heap[i], heap[p]];
      i = p;
    }
  }

  function heapPop() {
    if (heap.length === 0) return null;
    const top = heap[0];
    const last = heap.pop();
    if (heap.length > 0) {
      heap[0] = last;
      let i = 0;
      const n = heap.length;
      while (true) {
        let left = i * 2 + 1;
        let right = left + 1;
        let smallest = i;
        if (left < n) {
          if (heap[left].val < heap[smallest].val ||
              (heap[left].val === heap[smallest].val && heap[left].idx < heap[smallest].idx)) {
            smallest = left;
          }
        }
        if (right < n) {
          if (heap[right].val < heap[smallest].val ||
              (heap[right].val === heap[smallest].val && heap[right].idx < heap[smallest].idx)) {
            smallest = right;
          }
        }
        if (smallest === i) break;
        [heap[i], heap[smallest]] = [heap[smallest], heap[i]];
        i = smallest;
      }
    }
    return top;
  }

  // Initialize heap with first node of each non-empty list
  for (let i = 0; i < lists.length; i++) {
    const node = lists[i];
    if (node !== null && node !== undefined) {
      heapPush({ val: node.val, idx: i, node });
    }
  }

  const dummy = new ListNode();
  let tail = dummy;

  while (heap.length > 0) {
    const { node } = heapPop();
    tail.next = node;
    tail = node;
    if (node.next) {
      heapPush({ val: node.next.val, idx: 0, node: node.next });
      // idx is irrelevant after first push; using 0 keeps tie-breaking stable
    }
  }

  return dummy.next;
}
