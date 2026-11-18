class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n) time, O(h) space where n is number of nodes and h is tree height
function hasPathSum(root, target) {
  if (root === null) {
    return false;
  }
  if (root.left === null && root.right === null) {
    return root.val === target;
  }
  const rest = target - root.val;
  return hasPathSum(root.left, rest) || hasPathSum(root.right, rest);
}

// Call hasPathSum(...) here and console.log the result to try it.
