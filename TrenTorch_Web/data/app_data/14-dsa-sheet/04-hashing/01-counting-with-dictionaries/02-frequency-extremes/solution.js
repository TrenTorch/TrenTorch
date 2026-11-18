// O(n) time, O(n) space
function frequencyExtremes(nums) {
  const counts = new Map();
  for (const num of nums) {
    counts.set(num, (counts.get(num) || 0) + 1);
  }

  let mostVal = null;
  let mostCnt = -1;
  let leastVal = null;
  let leastCnt = Infinity;

  for (const [val, cnt] of counts.entries()) {
    if (mostVal === null || cnt > mostCnt || (cnt === mostCnt && val < mostVal)) {
      mostVal = val;
      mostCnt = cnt;
    }
    if (leastVal === null || cnt < leastCnt || (cnt === leastCnt && val < leastVal)) {
      leastVal = val;
      leastCnt = cnt;
    }
  }

  return [mostVal, leastVal];
}

console.log(frequencyExtremes([4, 4, 5, 5, 6]));
