// O(|s| + |t|) time, O(|t|) space
function minWindow(s, t) {
  if (!t) return "";
  const need = new Map();
  for (const ch of t) {
    need.set(ch, (need.get(ch) ?? 0) + 1);
  }
  const have = new Map();
  let missing = need.size;
  let bestStart = 0;
  let bestLen = s.length + 1;
  let left = 0;

  for (let right = 0; right < s.length; right++) {
    const ch = s[right];
    have.set(ch, (have.get(ch) ?? 0) + 1);
    if (need.has(ch) && have.get(ch) === need.get(ch)) {
      missing--;
    }
    while (missing === 0) {
      if (right - left + 1 < bestLen) {
        bestStart = left;
        bestLen = right - left + 1;
      }
      const gone = s[left];
      have.set(gone, have.get(gone) - 1);
      if (need.has(gone) && have.get(gone) < need.get(gone)) {
        missing++;
      }
      left++;
    }
  }
  return bestLen <= s.length ? s.substring(bestStart, bestStart + bestLen) : "";
}

console.log(minWindow("ADOBECODEBANC", "ABC"));
