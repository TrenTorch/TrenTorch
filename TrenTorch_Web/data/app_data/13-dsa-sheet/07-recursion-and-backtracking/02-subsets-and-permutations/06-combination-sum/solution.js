// Exponential time complexity, O(target/minCandidate) recursion depth, O(resultSize) space
function combinationSum(candidates, target) {
  const a = candidates.slice().sort((x, y) => x - y);
  const out = [];

  function go(start, remaining, current) {
    if (remaining === 0) {
      out.push(current.slice());
      return;
    }
    for (let j = start; j < a.length; j++) {
      if (a[j] > remaining) break;
      current.push(a[j]);
      go(j, remaining - a[j], current);
      current.pop();
    }
  }

  go(0, target, []);
  return out;
}

console.log(combinationSum([2, 3, 6, 7], 7));
