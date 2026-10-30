class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n) time, O(h) space where h is the tree height
function minDiffBst(root) {
  let best = Infinity;
  let prev = null;
  const stack = [];
  let node = root;
  while (node || stack.length) {
    while (node) {
      stack.push(node);
      node = node.left;
    }
    node = stack.pop();
    if (prev !== null) {
      const diff = node.val - prev;
      if (diff < best) best = diff;
    }
    prev = node.val;
    node = node.right;
  }
  return best;
}

// Call minDiffBst(...) here and console.log the result to try it.
