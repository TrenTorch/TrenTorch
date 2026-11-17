class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

/**
 * Builds a binary tree from a level-order array where null denotes missing children.
 * @param {Array} arr
 * @returns {TreeNode|null}
 */
function buildTreeFromArray(arr) {
  if (!arr.length) return null;
  const root = new TreeNode(arr[0]);
  const queue = [root];
  let i = 1;
  while (i < arr.length) {
    const node = queue.shift();
    if (!node) continue;

    const leftVal = arr[i++];
    if (leftVal != null) {
      node.left = new TreeNode(leftVal);
      queue.push(node.left);
    }

    if (i < arr.length) {
      const rightVal = arr[i++];
      if (rightVal != null) {
        node.right = new TreeNode(rightVal);
        queue.push(node.right);
      }
    }
  }
  return root;
}

// O(h) time, O(1) space where h is the tree height
function floorAndCeilBst(root, x) {
  if (Array.isArray(root)) {
    root = buildTreeFromArray(root);
  }
  let floor = -1;
  let ceil = -1;
  let node = root;
  while (node) {
    if (node.val === x) {
      return [x, x];
    }
    if (node.val < x) {
      floor = node.val;
      node = node.right;
    } else {
      ceil = node.val;
      node = node.left;
    }
  }
  return [floor, ceil];
}

// Example usage:
// const rootArray = [8, 4, 12, 2, 6, 10, 14];
// console.log(floorAndCeilBst(rootArray, 5)); // [4, 6]
