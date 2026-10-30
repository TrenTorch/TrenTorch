// O(n^2) time, O(n) space where n is the number of rows
function minimumTotal(triangle) {
  if (!triangle || triangle.length === 0) {
    return 0;
  }
  const best = [...triangle[triangle.length - 1]];
  for (let row = triangle.length - 2; row >= 0; row--) {
    for (let j = 0; j <= row; j++) {
      best[j] = triangle[row][j] + Math.min(best[j], best[j + 1]);
    }
  }
  return best[0];
}

console.log(minimumTotal([[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]));
