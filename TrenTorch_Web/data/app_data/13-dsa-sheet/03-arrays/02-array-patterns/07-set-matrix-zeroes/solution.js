// O(rows * cols) time, O(rows + cols) space
function setMatrixZeroes(matrix) {
  const rows = new Set();
  const cols = new Set();
  for (let i = 0; i < matrix.length; i++) {
    for (let j = 0; j < matrix[i].length; j++) {
      if (matrix[i][j] === 0) {
        rows.add(i);
        cols.add(j);
      }
    }
  }
  const result = [];
  for (let i = 0; i < matrix.length; i++) {
    const newRow = [];
    for (let j = 0; j < matrix[i].length; j++) {
      if (rows.has(i) || cols.has(j)) {
        newRow.push(0);
      } else {
        newRow.push(matrix[i][j]);
      }
    }
    result.push(newRow);
  }
  return result;
}

console.log(setMatrixZeroes([[1, 2, 3], [4, 0, 6], [7, 8, 9]]));
