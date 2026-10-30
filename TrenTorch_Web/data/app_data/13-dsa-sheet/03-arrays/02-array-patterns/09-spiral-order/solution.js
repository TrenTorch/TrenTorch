function spiralOrder(matrix) {
  // O(m*n) time, O(m*n) space where m=rows, n=cols
  if (!matrix || matrix.length === 0 || matrix[0].length === 0) {
    return [];
  }
  const out = [];
  let top = 0;
  let bottom = matrix.length - 1;
  let left = 0;
  let right = matrix[0].length - 1;

  while (top <= bottom && left <= right) {
    // top row: left to right
    out.push(...matrix[top].slice(left, right + 1));
    // right column: top+1 to bottom
    for (let i = top + 1; i <= bottom; i++) {
      out.push(matrix[i][right]);
    }
    // bottom row: right-1 to left (if there is more than one row)
    if (top < bottom) {
      for (let j = right - 1; j >= left; j--) {
        out.push(matrix[bottom][j]);
      }
    }
    // left column: bottom-1 to top+1 (if there is more than one column)
    if (left < right) {
      for (let i = bottom - 1; i > top; i--) {
        out.push(matrix[i][left]);
      }
    }
    top++;
    bottom--;
    left++;
    right--;
  }
  return out;
}

console.log(spiralOrder([[1, 2, 3], [4, 5, 6], [7, 8, 9]]));
