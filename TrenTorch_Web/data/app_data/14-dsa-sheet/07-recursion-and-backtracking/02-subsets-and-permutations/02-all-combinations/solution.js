// O(C(n,k) * k) time, O(k) space (excluding output)
function allCombinations(n, k) {
  const out = [];

  function go(start, current) {
    const need = k - current.length;
    if (need === 0) {
      out.push([...current]);
      return;
    }
    for (let j = start; j <= n - need + 1; j++) {
      current.push(j);
      go(j + 1, current);
      current.pop();
    }
  }

  go(1, []);
  return out;
}

console.log(allCombinations(4, 2));
