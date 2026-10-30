class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

/** Build a binary tree from a level‑order array where null/undefined denotes a missing child. */
function buildTree(arr) {
  if (!arr || arr.length === 0) return null;
  const root = new TreeNode(arr[0]);
  const queue = [{ node: root, idx: 0 }];
  let qPos = 0;
  while (qPos < queue.length) {
    const { node, idx } = queue[qPos++];
    const leftIdx = 2 * idx + 1;
    const rightIdx = 2 * idx + 2;
    if (leftIdx < arr.length && arr[leftIdx] != null) {
      node.left = new TreeNode(arr[leftIdx]);
      queue.push({ node: node.left, idx: leftIdx });
    }
    if (rightIdx < arr.length && arr[rightIdx] != null) {
      node.right = new TreeNode(arr[rightIdx]);
      queue.push({ node: node.right, idx: rightIdx });
    }
  }
  return root;
}

// O(n) time, O(h) space
function maxDepth(root) {
  if (Array.isArray(root)) {
    root = buildTree(root);
  }
  if (root == null) {
    return 0;
  }
  return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
}

// Call maxDepth(...) here and console.log the result to try it.
