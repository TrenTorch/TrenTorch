class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n) time, O(h) space
function bstFromPreorder(preorder) {
  let index = 0;

  function build(bound) {
    if (index === preorder.length || preorder[index] > bound) {
      return null;
    }
    const val = preorder[index];
    index++;
    const node = new TreeNode(val);
    node.left = build(val);
    node.right = build(bound);
    return node;
  }

  return build(Infinity);
}

console.log(bstFromPreorder([8, 5, 1, 7, 10, 12]));
