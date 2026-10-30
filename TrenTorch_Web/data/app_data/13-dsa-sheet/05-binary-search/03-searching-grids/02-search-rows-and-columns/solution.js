// O(min(m, n) * log(max(m, n))) time, O(log(m * n)) space
function searchMatrixIi(matrix, target) {
  if (!matrix || !matrix[0]) {
    return false;
  }

  function search(r0, r1, c0, c1) {
    if (r0 > r1 || c0 > c1) {
      return false;
    }
    if (r1 - r0 <= c1 - c0) {
      const r = Math.floor((r0 + r1) / 2);
      let lo = c0;
      let hi = c1 + 1;
      while (lo < hi) {
        const mid = Math.floor((lo + hi) / 2);
        if (matrix[r][mid] < target) {
          lo = mid + 1;
        } else {
          hi = mid;
        }
      }
      if (lo <= c1 && matrix[r][lo] === target) {
        return true;
      }
      return search(r0, r - 1, lo, c1) || search(r + 1, r1, c0, lo - 1);
    } else {
      const c = Math.floor((c0 + c1) / 2);
      let lo = r0;
      let hi = r1 + 1;
      while (lo < hi) {
        const mid = Math.floor((lo + hi) / 2);
        if (matrix[mid][c] < target) {
          lo = mid + 1;
        } else {
          hi = mid;
        }
      }
      if (lo <= r1 && matrix[lo][c] === target) {
        return true;
      }
      return search(r0, lo - 1, c + 1, c1) || search(lo, r1, c0, c - 1);
    }
  }

  return search(0, matrix.length - 1, 0, matrix[0].length - 1);
}

console.log(searchMatrixIi([[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16], [10, 13, 14, 17]], 5));
