// O(n^2) time, O(n^2) space
function palindromePartitions(s) {
  const n = s.length;
  const pal = Array.from({ length: n }, () => Array(n).fill(false));
  for (let len = 1; len <= n; len++) {
    for (let i = 0; i + len - 1 < n; i++) {
      const j = i + len - 1;
      pal[i][j] = s[i] === s[j] && (len <= 2 || pal[i + 1][j - 1]);
    }
  }
  const out = [];

  function go(start, pieces) {
    if (start === n) {
      out.push(pieces.slice());
      return;
    }
    for (let j = start; j < n; j++) {
      if (pal[start][j]) {
        pieces.push(s.slice(start, j + 1));
        go(j + 1, pieces);
        pieces.pop();
      }
    }
  }

  go(0, []);
  return out;
}

console.log(palindromePartitions("aab"));
