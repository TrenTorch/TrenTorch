// Write lowestCommonAncestor as the problem statement describes.
// O(n) time, O(h) space where h is tree height (recursion stack)
function lowestCommonAncestor(root, p, q) {
  if (root === null || root.val === p || root.val === q) {
    return root;
  }
  const left = lowestCommonAncestor(root.left, p, q);
  const right = lowestCommonAncestor(root.right, p, q);
  if (left && right) {
    return root;
  }
  return left || right;
}
