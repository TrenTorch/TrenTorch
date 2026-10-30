class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n) time, O(n) space
function balanceBst(root) {
  const values = [];
  const stack = [];
  let node = root;
  while (node || stack.length) {
    while (node) {
      stack.push(node);
      node = node.left;
    }
    node = stack.pop();
    values.push(node.val);
    node = node.right;
  }

  function build(lo, hi) {
    if (lo > hi) return null;
    const mid = Math.floor((lo + hi) / 2);
    const left = build(lo, mid - 1);
    const right = build(mid + 1, hi);
    return new TreeNode(values[mid], left, right);
  }

  return build(0, values.length - 1);
}

// Call balanceBst(...) here and console.log the result to try it.
