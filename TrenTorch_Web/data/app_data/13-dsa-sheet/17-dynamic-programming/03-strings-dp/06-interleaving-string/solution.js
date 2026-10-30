// O(m * n) time, O(n) space where m = a.length, n = b.length
function isInterleave(a, b, c) {
  if (a.length + b.length !== c.length) {
    return false;
  }
  const row = new Array(b.length + 1).fill(false);
  row[0] = true;
  for (let j = 1; j <= b.length; j++) {
    row[j] = row[j - 1] && b[j - 1] === c[j - 1];
  }
  for (let i = 1; i <= a.length; i++) {
    row[0] = row[0] && a[i - 1] === c[i - 1];
    for (let j = 1; j <= b.length; j++) {
      row[j] = (row[j] && a[i - 1] === c[i + j - 1]) ||
               (row[j - 1] && b[j - 1] === c[i + j - 1]);
    }
  }
  return row[b.length];
}

console.log(isInterleave("aabcc", "dbbca", "aadbbcbcac"));
