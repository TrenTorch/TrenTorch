// O(m*n) time, O(m*n) space
function transposeMatrix(matrix) {
  if (!matrix.length || !matrix[0].length) return [];
  const rows = matrix.length;
  const cols = matrix[0].length;
  const result = [];
  for (let j = 0; j < cols; j++) {
    const newRow = [];
    for (let i = 0; i < rows; i++) {
      newRow.push(matrix[i][j]);
    }
    result.push(newRow);
  }
  return result;
}

console.log(transposeMatrix([[1, 2, 3], [4, 5, 6]]));
