class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n) time, O(h) space where h is tree height (stack size)
function convertBst(root) {
  let total = 0;
  const stack = [];
  let node = root;
  while (node || stack.length) {
    while (node) {
      stack.push(node);
      node = node.right;
    }
    node = stack.pop();
    total += node.val;
    node.val = total;
    node = node.left;
  }
  return root;
}

// Call convertBst(...) here and console.log the result to try it.
