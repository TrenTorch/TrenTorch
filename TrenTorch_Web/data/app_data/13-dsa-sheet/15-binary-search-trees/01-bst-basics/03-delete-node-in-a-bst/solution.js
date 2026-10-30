class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(h) time, O(h) space where h is tree height (max 800)
function deleteNode(root, key) {
  if (root === null) {
    return null;
  }
  if (key < root.val) {
    root.left = deleteNode(root.left, key);
  } else if (key > root.val) {
    root.right = deleteNode(root.right, key);
  } else {
    if (root.left === null) {
      return root.right;
    }
    if (root.right === null) {
      return root.left;
    }
    let successor = root.right;
    while (successor.left !== null) {
      successor = successor.left;
    }
    root.val = successor.val;
    root.right = deleteNode(root.right, successor.val);
  }
  return root;
}

// Call deleteNode(...) here and console.log the result to try it.
