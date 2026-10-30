class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n) time, O(h) space where h is tree height
function kthSmallestBst(root, k) {
  const stack = [];
  let node = root;
  while (node != null || stack.length) {
    while (node != null) {
      stack.push(node);
      node = node.left;
    }
    node = stack.pop();
    k--;
    if (k === 0) {
      return node.val;
    }
    node = node.right;
  }
  return null; // should never reach here for valid input
}

// Call kthSmallestBst(...) here and console.log the result to try it.
