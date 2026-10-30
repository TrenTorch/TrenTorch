class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

function* ascending(node) {
  const stack = [];
  while (node || stack.length) {
    while (node) {
      stack.push(node);
      node = node.left;
    }
    node = stack.pop();
    yield node.val;
    node = node.right;
  }
}

function* descending(node) {
  const stack = [];
  while (node || stack.length) {
    while (node) {
      stack.push(node);
      node = node.right;
    }
    node = stack.pop();
    yield node.val;
    node = node.left;
  }
}

// O(n) time, O(h) space where h is tree height
function findTarget(root, k) {
  const upIter = ascending(root);
  const downIter = descending(root);

  let upNext = upIter.next();
  let downNext = downIter.next();

  let lo = upNext.done ? null : upNext.value;
  let hi = downNext.done ? null : downNext.value;

  while (lo !== null && hi !== null && lo < hi) {
    const sum = lo + hi;
    if (sum === k) return true;
    if (sum < k) {
      upNext = upIter.next();
      lo = upNext.done ? null : upNext.value;
    } else {
      downNext = downIter.next();
      hi = downNext.done ? null : downNext.value;
    }
  }
  return false;
}

// Call findTarget(...) here and console.log the result to try it.
