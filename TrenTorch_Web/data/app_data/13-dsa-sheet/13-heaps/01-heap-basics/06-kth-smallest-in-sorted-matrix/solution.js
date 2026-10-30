// O((rows + cols) * log(max - min)) time, O(1) space
function kthSmallestMatrix(matrix, k) {
  const rows = matrix.length;
  const cols = matrix[0].length;

  function countAtMost(x) {
    let count = 0;
    let col = cols - 1;
    for (let r = 0; r < rows; r++) {
      while (col >= 0 && matrix[r][col] > x) {
        col--;
      }
      count += col + 1;
    }
    return count;
  }

  let lo = matrix[0][0];
  let hi = matrix[rows - 1][cols - 1];
  while (lo < hi) {
    const mid = Math.floor((lo + hi) / 2);
    if (countAtMost(mid) >= k) {
      hi = mid;
    } else {
      lo = mid + 1;
    }
  }
  return lo;
}

console.log(kthSmallestMatrix([[1, 5, 9], [10, 11, 13], [12, 13, 15]], 8));
