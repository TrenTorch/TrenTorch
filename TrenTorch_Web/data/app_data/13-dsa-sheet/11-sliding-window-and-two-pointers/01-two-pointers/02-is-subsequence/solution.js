// O(n) time, O(1) space
function isSubsequence(s, t) {
  let i = 0;
  for (const ch of t) {
    if (i < s.length && s[i] === ch) {
      i++;
    }
  }
  return i === s.length;
}

console.log(isSubsequence("ace", "abcde"));
