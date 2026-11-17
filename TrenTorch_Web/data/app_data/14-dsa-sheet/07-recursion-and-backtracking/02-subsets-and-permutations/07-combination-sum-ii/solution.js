// O(2^n) time, O(n) space
function combinationSumIi(candidates, target) {
  const a = [...candidates].sort((x, y) => x - y);
  const out = [];

  function go(start, remaining, current) {
    if (remaining === 0) {
      out.push([...current]);
      return;
    }
    for (let j = start; j < a.length; j++) {
      if (j > start && a[j] === a[j - 1]) continue;
      if (a[j] > remaining) break;
      current.push(a[j]);
      go(j + 1, remaining - a[j], current);
      current.pop();
    }
  }

  go(0, target, []);
  return out;
}

console.log(combinationSumIi([10, 1, 2, 7, 6, 1, 5], 8));
