// O(n) time, O(1) space
function isAnagram(a, b) {
  if (a.length !== b.length) return false;
  const counts = new Array(26).fill(0);
  const base = "a".charCodeAt(0);
  for (let i = 0; i < a.length; i++) {
    counts[a.charCodeAt(i) - base]++;
    counts[b.charCodeAt(i) - base]--;
  }
  for (let i = 0; i < 26; i++) {
    if (counts[i] !== 0) return false;
  }
  return true;
}

console.log(isAnagram("listen", "silent"));
