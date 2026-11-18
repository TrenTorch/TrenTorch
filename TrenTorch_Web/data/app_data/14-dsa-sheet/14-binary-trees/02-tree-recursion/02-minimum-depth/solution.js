class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n) time, O(n) space
function minDepth(root) {
  // If the input is a level-order array, build the tree first
  if (Array.isArray(root)) {
    const arr = root;
    if (arr.length === 0) return 0;
    const nodes = arr.map(v => (v !== null && v !== undefined ? new TreeNode(v) : null));
    for (let i = 0; i < nodes.length; i++) {
      const node = nodes[i];
      if (!node) continue;
      const leftIdx = 2 * i + 1;
      const rightIdx = 2 * i + 2;
      if (leftIdx < nodes.length) node.left = nodes[leftIdx];
      if (rightIdx < nodes.length) node.right = nodes[rightIdx];
    }
    root = nodes[0];
  }

  if (root == null) return 0;
  const queue = [{ node: root, depth: 1 }];
  let idx = 0;
  while (idx < queue.length) {
    const { node, depth } = queue[idx++];
    if (!node.left && !node.right) {
      return depth;
    }
    if (node.left) queue.push({ node: node.left, depth: depth + 1 });
    if (node.right) queue.push({ node: node.right, depth: depth + 1 });
  }
  return 0;
}

// Call minDepth(...) here and console.log the result to try it.
