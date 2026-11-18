class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(h) time, O(1) space
function searchBst(root, val) {
  let node = root;
  while (node !== null && node.val !== val) {
    if (val < node.val) {
      node = node.left;
    } else {
      node = node.right;
    }
  }
  return node;
}

// Call searchBst(...) here and console.log the result to try it.
