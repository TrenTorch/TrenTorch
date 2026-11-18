// Write inorderSuccessor as the problem statement describes.
// O(h) time, O(1) space where h is the height of the tree
function inorderSuccessor(root, p) {
  let answer = null;
  let node = root;
  while (node) {
    if (node.val > p) {
      answer = node;
      node = node.left;
    } else {
      node = node.right;
    }
  }
  return answer;
}
