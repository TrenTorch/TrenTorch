// O(N + A log A) time, O(A) space where N is total characters, A is alphabet size (<=26)
function alienOrder(words) {
  // Collect all unique letters
  const lettersSet = new Set();
  for (const word of words) {
    for (const ch of word) {
      lettersSet.add(ch);
    }
  }
  const letters = Array.from(lettersSet).sort();

  // Build adjacency list and indegree map
  const adj = {};
  const inDegree = {};
  for (const ch of letters) {
    adj[ch] = new Set();
    inDegree[ch] = 0;
  }

  for (let i = 0; i < words.length - 1; i++) {
    const a = words[i];
    const b = words[i + 1];
    let foundDiff = false;
    const minLen = Math.min(a.length, b.length);
    for (let j = 0; j < minLen; j++) {
      if (a[j] !== b[j]) {
        const x = a[j];
        const y = b[j];
        if (!adj[x].has(y)) {
          adj[x].add(y);
          inDegree[y]++;
        }
        foundDiff = true;
        break;
      }
    }
    if (!foundDiff && a.length > b.length) {
      return "";
    }
  }

  // Min-heap implementation
  class MinHeap {
    constructor() {
      this.heap = [];
    }
    push(val) {
      this.heap.push(val);
      this.bubbleUp(this.heap.length - 1);
    }
    pop() {
      if (this.heap.length === 0) return null;
      const min = this.heap[0];
      const end = this.heap.pop();
      if (this.heap.length > 0) {
        this.heap[0] = end;
        this.bubbleDown(0);
      }
      return min;
    }
    size() {
      return this.heap.length;
    }
    bubbleUp(idx) {
      while (idx > 0) {
        const parentIdx = Math.floor((idx - 1) / 2);
        if (this.heap[parentIdx] <= this.heap[idx]) break;
        [this.heap[parentIdx], this.heap[idx]] = [this.heap[idx], this.heap[parentIdx]];
        idx = parentIdx;
      }
    }
    bubbleDown(idx) {
      const length = this.heap.length;
      while (true) {
        let smallest = idx;
        const left = 2 * idx + 1;
        const right = 2 * idx + 2;
        if (left < length && this.heap[left] < this.heap[smallest]) smallest = left;
        if (right < length && this.heap[right] < this.heap[smallest]) smallest = right;
        if (smallest === idx) break;
        [this.heap[idx], this.heap[smallest]] = [this.heap[smallest], this.heap[idx]];
        idx = smallest;
      }
    }
  }

  const heap = new MinHeap();
  for (const ch of letters) {
    if (inDegree[ch] === 0) {
      heap.push(ch);
    }
  }

  const out = [];
  while (heap.size() > 0) {
    const ch = heap.pop();
    out.push(ch);
    for (const nxt of adj[ch]) {
      inDegree[nxt]--;
      if (inDegree[nxt] === 0) {
        heap.push(nxt);
      }
    }
  }

  return out.length === letters.length ? out.join("") : "";
}

console.log(alienOrder(["wrt", "wrf", "er", "ett", "rftt"]));
