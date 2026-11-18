class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n) time, O(h) space
function maxPathSum(root) {
  let best = root.val;

  function gain(node) {
    if (node === null) return 0;
    const left = Math.max(0, gain(node.left));
    const right = Math.max(0, gain(node.right));
    best = Math.max(best, node.val + left + right);
    return node.val + Math.max(left, right);
  }

  gain(root);
  return best;
}

// Call maxPathSum(...) here and console.log the result to try it.
