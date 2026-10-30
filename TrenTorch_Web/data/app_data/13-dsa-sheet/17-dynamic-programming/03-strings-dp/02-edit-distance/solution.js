// O(|a|·|b|) time, O(min(|a|,|b|)) space
function editDistance(a, b) {
  if (b.length > a.length) {
    const temp = a;
    a = b;
    b = temp;
  }
  const m = a.length;
  const n = b.length;
  let prev = new Array(n + 1);
  for (let j = 0; j <= n; j++) {
    prev[j] = j;
  }
  for (let i = 1; i <= m; i++) {
    const cur = new Array(n + 1);
    cur[0] = i;
    for (let j = 1; j <= n; j++) {
      if (a[i - 1] === b[j - 1]) {
        cur[j] = prev[j - 1];
      } else {
        const replace = prev[j - 1];
        const deleteOp = prev[j];
        const insert = cur[j - 1];
        cur[j] = 1 + Math.min(replace, deleteOp, insert);
      }
    }
    prev = cur;
  }
  return prev[n];
}

console.log(editDistance("horse", "ros"));
