class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n) time, O(h) space
function recoverTree(root) {
  let first = null;
  let second = null;
  let prev = null;
  const stack = [];
  let node = root;

  while (node || stack.length > 0) {
    while (node) {
      stack.push(node);
      node = node.left;
    }
    node = stack.pop();
    if (prev !== null && prev.val > node.val) {
      if (first === null) {
        first = prev;
      }
      second = node;
    }
    prev = node;
    node = node.right;
  }

  if (first && second) {
    const temp = first.val;
    first.val = second.val;
    second.val = temp;
  }
  return root;
}

// Call recoverTree(...) here and console.log the result to try it.
