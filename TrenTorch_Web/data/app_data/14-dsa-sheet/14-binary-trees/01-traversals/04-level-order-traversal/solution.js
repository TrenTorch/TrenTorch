class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n) time, O(n) space
function levelOrder(root) {
  const out = [];
  if (!root) return out;
  const queue = [root];
  let head = 0;
  while (head < queue.length) {
    const levelSize = queue.length - head;
    const level = [];
    for (let i = 0; i < levelSize; i++) {
      const node = queue[head++];
      level.push(node.val);
      if (node.left) queue.push(node.left);
      if (node.right) queue.push(node.right);
    }
    out.push(level);
  }
  return out;
}

// Call levelOrder(...) here and console.log the result to try it.
