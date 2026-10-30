// O(n + m) time, O(1) space
function checkInclusion(s1, s2) {
  const m = s1.length;
  if (m > s2.length) return false;
  const need = new Array(26).fill(0);
  const window = new Array(26).fill(0);
  for (const ch of s1) {
    need[ch.charCodeAt(0) - 97]++;
  }
  for (let i = 0; i < s2.length; i++) {
    const ch = s2[i];
    window[ch.charCodeAt(0) - 97]++;
    if (i >= m) {
      const leftCh = s2[i - m];
      window[leftCh.charCodeAt(0) - 97]--;
    }
    if (i >= m - 1) {
      let match = true;
      for (let j = 0; j < 26; j++) {
        if (window[j] !== need[j]) {
          match = false;
          break;
        }
      }
      if (match) return true;
    }
  }
  return m === 0;
}

console.log(checkInclusion("ab", "eidbaooo"));
