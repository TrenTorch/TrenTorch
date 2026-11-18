class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n) time, O(h) space where h is the tree height
function largestBstSubtree(root) {
  let best = 0;
  const INF = Infinity;

  function go(node) {
    if (node === null) {
      return [0, INF, -INF];
    }
    const [leftSize, leftLow, leftHigh] = go(node.left);
    const [rightSize, rightLow, rightHigh] = go(node.right);

    if (leftSize >= 0 && rightSize >= 0 && leftHigh < node.val && node.val < rightLow) {
      const size = leftSize + rightSize + 1;
      if (size > best) best = size;
      const low = Math.min(leftLow, node.val);
      const high = Math.max(rightHigh, node.val);
      return [size, low, high];
    }
    return [-1, -Infinity, Infinity];
  }

  go(root);
  return best;
}

// Call largestBstSubtree(...) here and console.log the result to try it.
