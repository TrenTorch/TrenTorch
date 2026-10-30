class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n) time, O(n) space
function burnTime(root, start) {
  const parent = new Map();
  let origin = null;
  const stack = [[root, null]];
  while (stack.length > 0) {
    const [node, par] = stack.pop();
    if (!node) continue;
    parent.set(node, par);
    if (node.val === start) {
      origin = node;
    }
    if (node.left) stack.push([node.left, node]);
    if (node.right) stack.push([node.right, node]);
  }
  // Safety: if origin not found (should not happen), return 0
  if (!origin) return 0;
  const seen = new Set();
  seen.add(origin);
  const queue = [origin];
  let head = 0;
  let minutes = -1;
  while (head < queue.length) {
    minutes++;
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
  return minutes;
}

// Call burnTime(...) here and console.log the result to try it.
