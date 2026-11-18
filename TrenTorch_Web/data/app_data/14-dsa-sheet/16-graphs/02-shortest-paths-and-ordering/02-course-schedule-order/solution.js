// O(n log n) time, O(n) space
function findOrder(numCourses, prerequisites) {
  // Build adjacency list and indegree array
  const adj = Array.from({ length: numCourses }, () => []);
  const indegree = new Array(numCourses).fill(0);
  for (const [course, pre] of prerequisites) {
    adj[pre].push(course);
    indegree[course] += 1;
  }

  // Min-heap implementation
  const heap = [];
  // Initialize heap with nodes of indegree 0
  for (let i = 0; i < numCourses; i++) {
    if (indegree[i] === 0) heapPush(heap, i);
  }

  const order = [];
  while (heap.length > 0) {
    const node = heapPop(heap);
    order.push(node);
    for (const nxt of adj[node]) {
      indegree[nxt] -= 1;
      if (indegree[nxt] === 0) {
        heapPush(heap, nxt);
      }
    }
  }

  return order.length === numCourses ? order : [];
}

// Heap helper functions (min-heap)
function heapPush(heap, value) {
  heap.push(value);
  let idx = heap.length - 1;
  while (idx > 0) {
    const parent = (idx - 1) >> 1;
    if (heap[parent] <= heap[idx]) break;
    [heap[parent], heap[idx]] = [heap[idx], heap[parent]];
    idx = parent;
  }
}

function heapPop(heap) {
  const top = heap[0];
  const last = heap.pop();
  if (heap.length > 0) {
    heap[0] = last;
    heapifyDown(heap, 0);
  }
  return top;
}

function heapifyDown(heap, idx) {
  const n = heap.length;
  while (true) {
    let left = idx * 2 + 1;
    let right = left + 1;
    let smallest = idx;
    if (left < n && heap[left] < heap[smallest]) smallest = left;
    if (right < n && heap[right] < heap[smallest]) smallest = right;
    if (smallest === idx) break;
    [heap[idx], heap[smallest]] = [heap[smallest], heap[idx]];
    idx = smallest;
  }
}

// Test example
console.log(findOrder(4, [[1, 0], [2, 0], [3, 1], [3, 2]]));
