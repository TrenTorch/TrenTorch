class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n) time, O(1) space
function flattenTree(root) {
  let node = root;
  while (node) {
    if (node.left) {
      let tail = node.left;
      while (tail.right) {
        tail = tail.right;
      }
      tail.right = node.right;
      node.right = node.left;
      node.left = null;
    }
    node = node.right;
  }
  return root;
}

// Call flattenTree(...) here and console.log the result to try it.
