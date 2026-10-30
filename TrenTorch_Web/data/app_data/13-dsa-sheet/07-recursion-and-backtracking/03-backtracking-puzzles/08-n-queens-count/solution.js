// O(n!) time, O(n) space
function nQueensCount(n) {
  const cols = new Set();
  const diag1 = new Set();
  const diag2 = new Set();

  function go(r) {
    if (r === n) return 1;
    let total = 0;
    for (let c = 0; c < n; c++) {
      if (cols.has(c) || diag1.has(r - c) || diag2.has(r + c)) continue;
      cols.add(c);
      diag1.add(r - c);
      diag2.add(r + c);
      total += go(r + 1);
      cols.delete(c);
      diag1.delete(r - c);
      diag2.delete(r + c);
    }
    return total;
  }

  return go(0);
}

console.log(nQueensCount(4));
