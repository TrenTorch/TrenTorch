class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n) time, O(h) space
function trimBst(root, low, high) {
  if (root === null) {
    return null;
  }
  if (root.val < low) {
    return trimBst(root.right, low, high);
  }
  if (root.val > high) {
    return trimBst(root.left, low, high);
  }
  root.left = trimBst(root.left, low, high);
  root.right = trimBst(root.right, low, high);
  return root;
}

// Call trimBst(...) here and console.log the result to try it.
