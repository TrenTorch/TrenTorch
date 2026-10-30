// O(n*m) time, O(m) space
function isMatchWildcard(s, p) {
  const n = s.length;
  const m = p.length;
  let prev = new Array(m + 1).fill(false);
  prev[0] = true;
  for (let j = 1; j <= m; j++) {
    prev[j] = prev[j - 1] && p[j - 1] === '*';
  }
  for (let i = 1; i <= n; i++) {
    let cur = new Array(m + 1).fill(false);
    for (let j = 1; j <= m; j++) {
      if (p[j - 1] === '*') {
        cur[j] = cur[j - 1] || prev[j];
      } else if (p[j - 1] === '?' || p[j - 1] === s[i - 1]) {
        cur[j] = prev[j - 1];
      }
    }
    prev = cur;
  }
  return prev[m];
}

console.log(isMatchWildcard("aa", "*"));
