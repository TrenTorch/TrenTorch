// O(n) time, O(1) space
function findAnagrams(s, p) {
  const m = p.length;
  if (m === 0 || m > s.length) {
    return [];
  }
  const need = new Array(26).fill(0);
  const window = new Array(26).fill(0);
  for (const ch of p) {
    need[ch.charCodeAt(0) - 97]++;
  }
  const out = [];
  for (let i = 0; i < s.length; i++) {
    window[s.charCodeAt(i) - 97]++;
    if (i >= m) {
      window[s.charCodeAt(i - m) - 97]--;
    }
    if (i >= m - 1) {
      let match = true;
      for (let j = 0; j < 26; j++) {
        if (window[j] !== need[j]) {
          match = false;
          break;
        }
      }
      if (match) {
        out.push(i - m + 1);
      }
    }
  }
  return out;
}

console.log(findAnagrams("cbaebabacd", "abc"));
