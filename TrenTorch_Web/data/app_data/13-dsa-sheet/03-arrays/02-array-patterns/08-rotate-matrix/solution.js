// O(m*n) time, O(m*n) space
function rotateMatrix(matrix) {
  if (!matrix.length || !matrix[0].length) return [];
  const rows = matrix.length;
  const cols = matrix[0].length;
  const result = [];
  for (let c = 0; c < cols; c++) {
    const newRow = [];
    for (let r = rows - 1; r >= 0; r--) {
      newRow.push(matrix[r][c]);
    }
    result.push(newRow);
  }
  return result;
}

console.log(rotateMatrix([[1, 2, 3], [4, 5, 6]]));
