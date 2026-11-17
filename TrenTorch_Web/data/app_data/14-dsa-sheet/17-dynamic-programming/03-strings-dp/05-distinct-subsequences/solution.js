// O(n*m) time, O(m) space
function numDistinct(s, t) {
  const mod = 1000000007;
  const m = t.length;
  const row = new Array(m + 1).fill(0);
  row[0] = 1;
  for (const ch of s) {
    for (let j = m; j >= 1; j--) {
      if (t[j - 1] === ch) {
        row[j] = (row[j] + row[j - 1]) % mod;
      }
    }
  }
  return row[m];
}

console.log(numDistinct("rabbbit", "rabbit"));
