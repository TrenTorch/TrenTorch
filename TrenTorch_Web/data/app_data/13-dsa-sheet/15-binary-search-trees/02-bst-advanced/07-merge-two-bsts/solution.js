class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n1 + n2) time, O(n1 + n2) space
function mergeBsts(root1, root2) {
  function inorder(root) {
    const out = [];
    const stack = [];
    let node = root;
    while (node || stack.length) {
      while (node) {
        stack.push(node);
        node = node.left;
      }
      node = stack.pop();
      out.push(node.val);
      node = node.right;
    }
    return out;
  }

  const a = inorder(root1);
  const b = inorder(root2);
  const out = [];
  let i = 0, j = 0;
  while (i < a.length && j < b.length) {
    if (a[i] <= b[j]) {
      out.push(a[i]);
      i++;
    } else {
      out.push(b[j]);
      j++;
    }
  }
  while (i < a.length) out.push(a[i++]);
  while (j < b.length) out.push(b[j++]);
  return out;
}

// Call mergeBsts(...) here and console.log the result to try it.
