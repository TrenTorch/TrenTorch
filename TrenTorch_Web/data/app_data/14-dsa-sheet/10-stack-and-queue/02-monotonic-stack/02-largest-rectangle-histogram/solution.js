// O(n) time, O(n) space
function largestRectangle(heights) {
  let best = 0;
  const stack = [];
  const extended = [...heights, 0];
  for (let i = 0; i < extended.length; i++) {
    const h = extended[i];
    while (stack.length > 0 && extended[stack[stack.length - 1]] >= h) {
      const height = extended[stack.pop()];
      const left = stack.length > 0 ? stack[stack.length - 1] : -1;
      const width = i - left - 1;
      best = Math.max(best, height * width);
    }
    stack.push(i);
  }
  return best;
}

console.log(largestRectangle([2, 1, 5, 6, 2, 3]));
