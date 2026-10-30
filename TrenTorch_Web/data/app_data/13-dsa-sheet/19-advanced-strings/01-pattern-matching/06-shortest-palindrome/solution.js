// O(n) time, O(n) space
function shortestPalindrome(s) {
  const rev = s.split('').reverse().join('');
  const t = s + '#' + rev;
  const pi = new Array(t.length).fill(0);
  let k = 0;
  for (let i = 1; i < t.length; i++) {
    while (k > 0 && t[i] !== t[k]) {
      k = pi[k - 1];
    }
    if (t[i] === t[k]) {
      k++;
    }
    pi[i] = k;
  }
  const border = t.length > 0 ? pi[t.length - 1] : 0;
  const suffix = s.slice(border).split('').reverse().join('');
  return suffix + s;
}

console.log(shortestPalindrome("aacecaaa"));
