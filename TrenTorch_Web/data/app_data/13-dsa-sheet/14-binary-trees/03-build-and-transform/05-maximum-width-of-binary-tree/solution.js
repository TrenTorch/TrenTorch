class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n) time, O(n) space
function widthOfTree(root) {
  if (root === null) {
    return 0;
  }
  let best = 0;
  const queue = [[root, 0]];
  let head = 0;
  while (head < queue.length) {
    const levelSize = queue.length - head;
    const first = queue[head][1];
    let last = first;
    for (let i = 0; i < levelSize; i++) {
      const [node, index] = queue[head++];
      last = index;
      if (node.left !== null) {
        queue.push([node.left, 2 * index + 1]);
      }
      if (node.right !== null) {
        queue.push([node.right, 2 * index + 2]);
      }
    }
    best = Math.max(best, last - first + 1);
  }
  return best;
}

// Call widthOfTree(...) here and console.log the result to try it.
