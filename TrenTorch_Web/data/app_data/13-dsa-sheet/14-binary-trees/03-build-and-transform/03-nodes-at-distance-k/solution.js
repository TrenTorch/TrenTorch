class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n log n) time, O(n) space
function distanceK(root, target, k) {
  if (!root) return [];
  const parent = new Map();
  let start = null;
  const stack = [[root, null]];
  while (stack.length) {
    const [node, par] = stack.pop();
    parent.set(node, par);
    if (node.val === target) {
      start = node;
    }
    if (node.left) stack.push([node.left, node]);
    if (node.right) stack.push([node.right, node]);
  }
  if (!start) return [];
  const seen = new Set([start]);
  const queue = [start];
  let head = 0;
  for (let step = 0; step < k; step++) {
    const levelSize = queue.length - head;
    for (let i = 0; i < levelSize; i++) {
      const node = queue[head++];
      const neighbors = [node.left, node.right, parent.get(node)];
      for (const nxt of neighbors) {
        if (nxt && !seen.has(nxt)) {
          seen.add(nxt);
          queue.push(nxt);
        }
      }
    }
  }
  const result = [];
  for (let i = head; i < queue.length; i++) {
    result.push(queue[i].val);
  }
  result.sort((a, b) => a - b);
  return result;
}

// Call distanceK(...) here and console.log the result to try it.
