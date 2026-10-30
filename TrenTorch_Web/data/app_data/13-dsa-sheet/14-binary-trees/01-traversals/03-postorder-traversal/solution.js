class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n) time, O(n) space
function postorderTraversal(root) {
  const out = [];
  const stack = root ? [root] : [];
  while (stack.length > 0) {
    const node = stack.pop();
    out.push(node.val);
    if (node.left) stack.push(node.left);
    if (node.right) stack.push(node.right);
  }
  return out.reverse();
}

// Call postorderTraversal(...) here and console.log the result to try it.
