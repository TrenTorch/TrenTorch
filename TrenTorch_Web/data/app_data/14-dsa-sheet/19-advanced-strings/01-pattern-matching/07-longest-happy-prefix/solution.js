// O(n) time, O(n) space
function longestHappyPrefix(s) {
  const n = s.length;
  if (n === 0) return "";
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
  return s.slice(0, pi[n - 1]);
}

console.log(longestHappyPrefix("level"));
