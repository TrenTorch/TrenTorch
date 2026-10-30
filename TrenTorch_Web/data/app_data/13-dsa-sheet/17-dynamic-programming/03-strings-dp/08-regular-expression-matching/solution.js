// O(n*m) time, O(m) space where n = len(s), m = len(p)
function isMatchRegex(s, p) {
  const fits = (x, ch) => x === '.' || x === ch;
  let prev = new Array(p.length + 1).fill(false);
  prev[0] = true;
  for (let j = 2; j <= p.length; j++) {
    prev[j] = p[j - 1] === '*' && prev[j - 2];
  }
  for (let i = 1; i <= s.length; i++) {
    const cur = new Array(p.length + 1).fill(false);
    for (let j = 1; j <= p.length; j++) {
      if (p[j - 1] === '*') {
        cur[j] = cur[j - 2] || (fits(p[j - 2], s[i - 1]) && prev[j]);
      } else {
        cur[j] = fits(p[j - 1], s[i - 1]) && prev[j - 1];
      }
    }
    prev = cur;
  }
  return prev[p.length];
}

console.log(isMatchRegex("aab", "c*a*b"));
