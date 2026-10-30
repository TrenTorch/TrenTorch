class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n) time, O(h) space
function isSymmetric(root) {
  function mirror(a, b) {
    if (a === null && b === null) return true;
    if (a === null || b === null || a.val !== b.val) return false;
    return mirror(a.left, b.right) && mirror(a.right, b.left);
  }
  return root === null || mirror(root.left, root.right);
}

// Call isSymmetric(...) here and console.log the result to try it.
