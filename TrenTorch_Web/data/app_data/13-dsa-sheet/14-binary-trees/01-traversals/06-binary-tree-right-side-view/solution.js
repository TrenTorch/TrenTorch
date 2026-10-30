class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n) time, O(n) space
function rightSideView(root) {
  const out = [];
  if (!root) return out;
  const queue = [root];
  let head = 0;
  while (head < queue.length) {
    const levelSize = queue.length - head;
    let last;
    for (let i = 0; i < levelSize; i++) {
      const node = queue[head++];
      last = node.val;
      if (node.left) queue.push(node.left);
      if (node.right) queue.push(node.right);
    }
    out.push(last);
  }
  return out;
}

// Call rightSideView(...) here and console.log the result to try it.
