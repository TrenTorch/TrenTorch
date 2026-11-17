// O(rows + cols) time, O(1) extra space
function rowWithMostOnes(matrix) {
  let bestRow = -1;
  let col = matrix.length > 0 ? matrix[0].length : 0;
  for (let i = 0; i < matrix.length; i++) {
    const row = matrix[i];
    let moved = false;
    while (col > 0 && row[col - 1] === 1) {
      col--;
      moved = true;
    }
    if (moved) {
      bestRow = i;
    }
  }
  return bestRow;
}

console.log(rowWithMostOnes([[0, 0, 1, 1], [0, 1, 1, 1], [0, 0, 0, 1]]));
