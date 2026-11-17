// O(1) time, O(1) space (constant 32 iterations)
function longestOnesAfterFlip(n) {
  let best = 0;
  let current = 0;
  let previous = 0;
  for (let i = 0; i < 32; i++) {
    if ((n >>> i) & 1) {
      current++;
    } else {
      previous = current;
      current = 0;
    }
    best = Math.max(best, previous + current + 1);
  }
  return Math.min(best, 32);
}

console.log(longestOnesAfterFlip(1775));
