// O(n) time, O(min(n, charset)) space
function longestUniqueSubstring(s) {
  const last = new Map();
  let start = 0;
  let best = 0;
  for (let i = 0; i < s.length; i++) {
    const ch = s[i];
    if (last.has(ch) && last.get(ch) >= start) {
      start = last.get(ch) + 1;
    }
    last.set(ch, i);
    const currentLen = i - start + 1;
    if (currentLen > best) best = currentLen;
  }
  return best;
}

console.log(longestUniqueSubstring("abcabcbb"));
