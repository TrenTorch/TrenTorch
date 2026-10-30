class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n) time, O(h) space
function isValidBst(root) {
  function check(node, low, high) {
    if (node === null) return true;
    if (!(low < node.val && node.val < high)) return false;
    return check(node.left, low, node.val) && check(node.right, node.val, high);
  }
  return check(root, -Infinity, Infinity);
}

// Call isValidBst(...) here and console.log the result to try it.
console.log(isValidBst(new TreeNode(2, new TreeNode(1), new TreeNode(3)))); // true
console.log(isValidBst(new TreeNode(5, new TreeNode(1), new TreeNode(4, new TreeNode(3), new TreeNode(6))))); // false
