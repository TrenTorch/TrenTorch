class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n) time, O(h) space
function invertTree(root) {
  if (root === null) {
    return null;
  }
  const left = invertTree(root.right);
  const right = invertTree(root.left);
  root.left = left;
  root.right = right;
  return root;
}

// Call invertTree(...) here and console.log the result to try it.
