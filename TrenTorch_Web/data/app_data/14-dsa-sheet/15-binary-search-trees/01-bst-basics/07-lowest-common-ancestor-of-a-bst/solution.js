// Write lcaBst as the problem statement describes.
// O(h) time, O(1) space
function lcaBst(root, p, q) {
  let node = root;
  while (node) {
    if (p < node.val && q < node.val) {
      node = node.left;
    } else if (p > node.val && q > node.val) {
      node = node.right;
    } else {
      return node;
    }
  }
  return null;
}
