class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n) time, O(h) space where h is the tree height (recursion stack)
function rootToLeafPaths(root) {
  const out = [];
  const path = [];

  function go(node) {
    if (node === null) return;
    path.push(String(node.val));
    if (node.left === null && node.right === null) {
      out.push(path.join('->'));
    } else {
      go(node.left);
      go(node.right);
    }
    path.pop();
  }

  go(root);
  return out;
}

// Call rootToLeafPaths(...) here and console.log the result to try it.
