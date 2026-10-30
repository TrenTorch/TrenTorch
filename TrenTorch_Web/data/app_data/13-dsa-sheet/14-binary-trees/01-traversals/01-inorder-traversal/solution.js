class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n) time, O(h) space where h is tree height
function inorderTraversal(root) {
  const out = [];
  const stack = [];
  let node = root;
  while (node !== null || stack.length) {
    while (node !== null) {
      stack.push(node);
      node = node.left;
    }
    node = stack.pop();
    out.push(node.val);
    node = node.right;
  }
  return out;
}

// Call inorderTraversal(...) here and console.log the result to try it.
