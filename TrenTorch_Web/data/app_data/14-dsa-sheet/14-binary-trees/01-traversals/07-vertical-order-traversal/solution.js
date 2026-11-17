class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// O(n log n) time, O(n) space
function verticalOrder(root) {
  if (!root) return [];

  const columns = new Map(); // col -> array of [row, val]
  const queue = [{ node: root, row: 0, col: 0 }];
  let idx = 0;

  while (idx < queue.length) {
    const { node, row, col } = queue[idx++];
    if (!columns.has(col)) columns.set(col, []);
    columns.get(col).push([row, node.val]);

    if (node.left) {
      queue.push({ node: node.left, row: row + 1, col: col - 1 });
    }
    if (node.right) {
      queue.push({ node: node.right, row: row + 1, col: col + 1 });
    }
  }

  const sortedCols = Array.from(columns.keys()).sort((a, b) => a - b);
  const result = sortedCols.map(col => {
    const list = columns.get(col);
    list.sort((a, b) => {
      if (a[0] !== b[0]) return a[0] - b[0]; // sort by row
      return a[1] - b[1]; // then by value
    });
    return list.map(pair => pair[1]);
  });

  return result;
}

// Example usage:
// const root = new TreeNode(3,
//   new TreeNode(9),
//   new TreeNode(20, new TreeNode(15), new TreeNode(7))
// );
// console.log(verticalOrder(root));

console.log(verticalOrder(/* root */));
