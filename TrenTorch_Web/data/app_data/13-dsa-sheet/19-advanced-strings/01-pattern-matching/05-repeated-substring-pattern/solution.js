// O(n) time, O(n) space
function repeatedSubstringPattern(s) {
  const n = s.length;
  if (n < 2) return false;
  const pi = new Array(n).fill(0);
  let k = 0;
  for (let i = 1; i < n; i++) {
    while (k > 0 && s[i] !== s[k]) {
      k = pi[k - 1];
    }
    if (s[i] === s[k]) {
      k++;
    }
    pi[i] = k;
  }
  const period = n - pi[n - 1];
  return pi[n - 1] > 0 && n % period === 0;
}

console.log(repeatedSubstringPattern("abab"));
