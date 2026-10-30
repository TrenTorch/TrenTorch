class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n) time, O(h) space where h is the tree height
function isBalanced(root) {
  // If the input is a level‑order array, build a TreeNode structure first
  if (Array.isArray(root)) {
    root = buildTreeFromArray(root);
  }

  function check(node) {
    if (node === null) return 0;
    const left = check(node.left);
    if (left === -1) return -1;
    const right = check(node.right);
    if (right === -1 || Math.abs(left - right) > 1) return -1;
    return 1 + Math.max(left, right);
  }

  return check(root) !== -1;
}

// Helper: convert level‑order array (with null for missing nodes) to a binary tree
function buildTreeFromArray(arr) {
  if (!arr.length) return null;
  const root = new TreeNode(arr[0]);
  const queue = [root];
  let i = 1;
  while (i < arr.length) {
    const current = queue.shift();
    if (current !== null) {
      const leftVal = arr[i++];
      if (leftVal !== null && leftVal !== undefined) {
        current.left = new TreeNode(leftVal);
        queue.push(current.left);
      } else {
        current.left = null;
        queue.push(null);
      }
      if (i < arr.length) {
        const rightVal = arr[i++];
        if (rightVal !== null && rightVal !== undefined) {
          current.right = new TreeNode(rightVal);
          queue.push(current.right);
        } else {
          current.right = null;
          queue.push(null);
        }
      }
    }
  }
  return root;
}

// Example usage:
// const rootArray = [3, 9, 20, null, null, 15, 7];
// console.log(isBalanced(rootArray)); // true

// const rootArray2 = [1, 2, 2, 3, 3, null, null, 4, 4];
// console.log(isBalanced(rootArray2)); // false

// Call isBalanced(...) here and console.log the result to try it.
