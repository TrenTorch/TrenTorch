class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n) time, O(h) space
function rangeSumBst(root, low, high) {
  if (Array.isArray(root)) {
    root = buildTreeFromArray(root);
  }
  return dfs(root, low, high);
}

function dfs(node, low, high) {
  if (node === null) return 0;
  if (node.val < low) return dfs(node.right, low, high);
  if (node.val > high) return dfs(node.left, low, high);
  return node.val + dfs(node.left, low, high) + dfs(node.right, low, high);
}

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

// Call rangeSumBst(...) here and console.log the result to try it.
