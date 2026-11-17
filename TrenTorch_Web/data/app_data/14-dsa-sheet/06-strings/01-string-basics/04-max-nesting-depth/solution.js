// O(n) time, O(1) space
function maxNestingDepth(s) {
  let depth = 0;
  let best = 0;
  for (let ch of s) {
    if (ch === '(') {
      depth++;
      if (depth > best) best = depth;
    } else if (ch === ')') {
      depth--;
    }
  }
  return best;
}

console.log(maxNestingDepth("(1+(2*3)+((8)/4))+1"));
