class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n) time, O(n) space
function diameter(root) {
  let best = 0;

  function height(node) {
    if (node == null) return 0;
    const left = height(node.left);
    const right = height(node.right);
    best = Math.max(best, left + right);
    return 1 + Math.max(left, right);
  }

  height(root);
  return best;
}

// Call diameter(...) here and console.log the result to try it.
