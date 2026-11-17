class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(h) time, O(1) space where h is the height of the tree
function insertIntoBst(root, val) {
  if (root === null) {
    return new TreeNode(val);
  }
  let node = root;
  while (true) {
    if (val < node.val) {
      if (node.left === null) {
        node.left = new TreeNode(val);
        break;
      }
      node = node.left;
    } else {
      if (node.right === null) {
        node.right = new TreeNode(val);
        break;
      }
      node = node.right;
    }
  }
  return root;
}

// Call insertIntoBst(...) here and console.log the result to try it.
