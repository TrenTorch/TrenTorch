// O(rows * cols) time, O(cols) space
function maximalRectangle(matrix) {
  if (!matrix || matrix.length === 0) return 0;
  const cols = matrix[0].length;
  const heights = new Array(cols).fill(0);
  let best = 0;

  function largestInHistogram(hs) {
    let result = 0;
    const stack = [];
    for (let i = 0; i <= hs.length; i++) {
      const h = i === hs.length ? 0 : hs[i];
      while (stack.length && hs[stack[stack.length - 1]] >= h) {
        const height = hs[stack.pop()];
        const left = stack.length ? stack[stack.length - 1] : -1;
        result = Math.max(result, height * (i - left - 1));
      }
      stack.push(i);
    }
    return result;
  }

  for (const row of matrix) {
    for (let j = 0; j < cols; j++) {
      heights[j] = row[j] ? heights[j] + 1 : 0;
    }
    best = Math.max(best, largestInHistogram(heights));
  }
  return best;
}

console.log(maximalRectangle([[1, 0, 1, 0, 0], [1, 0, 1, 1, 1], [1, 1, 1, 1, 1], [1, 0, 0, 1, 0]]));
