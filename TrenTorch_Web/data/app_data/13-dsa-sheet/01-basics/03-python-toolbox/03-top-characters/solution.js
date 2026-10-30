// O(n log n) time, O(n) space
function topCharacters(s, k) {
  const freq = new Map();
  for (let i = 0; i < s.length; i++) {
    const ch = s[i];
    freq.set(ch, (freq.get(ch) || 0) + 1);
  }
  const entries = Array.from(freq.entries());
  entries.sort((a, b) => {
    if (b[1] !== a[1]) return b[1] - a[1];
    return a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0;
  });
  const limit = Math.min(k, entries.length);
  const result = [];
  for (let i = 0; i < limit; i++) {
    result.push([entries[i][0], entries[i][1]]);
  }
  return result;
}
