class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(h) time, O(1) space
function closestValue(root, target) {
  if (!root) return null;
  let best = root.val;
  let node = root;
  while (node) {
    const diff = Math.abs(node.val - target);
    const bestDiff = Math.abs(best - target);
    if (diff < bestDiff || (diff === bestDiff && node.val < best)) {
      best = node.val;
    }
    node = target < node.val ? node.left : node.right;
  }
  return best;
}

// Call closestValue(...) here and console.log the result to try it.
