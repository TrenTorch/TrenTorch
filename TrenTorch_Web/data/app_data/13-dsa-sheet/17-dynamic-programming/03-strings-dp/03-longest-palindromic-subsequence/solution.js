// O(n^2) time, O(n) space
function longestPalindromeSubseq(s) {
  const n = s.length;
  if (n === 0) return 0;
  let prev = new Array(n).fill(0);
  for (let i = n - 1; i >= 0; i--) {
    const cur = new Array(n).fill(0);
    cur[i] = 1;
    for (let j = i + 1; j < n; j++) {
      if (s[i] === s[j]) {
        cur[j] = 2 + (j - 1 >= 0 ? prev[j - 1] : 0);
      } else {
        cur[j] = Math.max(prev[j], cur[j - 1]);
      }
    }
    prev = cur;
  }
  return prev[n - 1];
}

console.log(longestPalindromeSubseq("bbbab"));
