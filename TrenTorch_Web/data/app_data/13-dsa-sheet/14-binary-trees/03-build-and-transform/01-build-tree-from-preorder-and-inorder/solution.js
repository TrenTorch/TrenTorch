class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n) time, O(n) space
function buildTree(preorder, inorder) {
  const inorderIndex = new Map();
  for (let i = 0; i < inorder.length; i++) {
    inorderIndex.set(inorder[i], i);
  }
  let preIndex = 0;

  function build(lo, hi) {
    if (lo >= hi) return null;
    const rootVal = preorder[preIndex++];
    const root = new TreeNode(rootVal);
    const mid = inorderIndex.get(rootVal);
    root.left = build(lo, mid);
    root.right = build(mid + 1, hi);
    return root;
  }

  return build(0, inorder.length);
}

console.log(buildTree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7]));
