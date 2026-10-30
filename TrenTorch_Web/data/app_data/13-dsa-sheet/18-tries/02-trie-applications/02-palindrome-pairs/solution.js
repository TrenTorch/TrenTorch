// O(n * L^2) time, O(n) space
function palindromePairs(words) {
  // Build map from word to list of indices
  const index = new Map();
  for (let i = 0; i < words.length; i++) {
    const w = words[i];
    if (!index.has(w)) index.set(w, []);
    index.get(w).push(i);
  }

  const found = new Set();

  const reverseStr = (s) => s.split('').reverse().join('');

  for (let i = 0; i < words.length; i++) {
    const w = words[i];
    const len = w.length;
    for (let cut = 0; cut <= len; cut++) {
      const prefix = w.slice(0, cut);
      const suffix = w.slice(cut);

      // If prefix is palindrome, look for reversed suffix
      if (prefix === reverseStr(prefix)) {
        const revSuffix = reverseStr(suffix);
        const candidates = index.get(revSuffix);
        if (candidates) {
          for (const j of candidates) {
            if (j !== i) {
              found.add(`${j},${i}`);
            }
          }
        }
      }

      // If suffix is palindrome, look for reversed prefix
      // Avoid duplicate work when cut == len (suffix empty) already handled above
      if (suffix === reverseStr(suffix)) {
        const revPrefix = reverseStr(prefix);
        const candidates = index.get(revPrefix);
        if (candidates) {
          for (const j of candidates) {
            if (j !== i) {
              found.add(`${i},${j}`);
            }
          }
        }
      }
    }
  }

  const result = Array.from(found, (s) => s.split(',').map(Number));
  result.sort((a, b) => (a[0] === b[0] ? a[1] - b[1] : a[0] - b[0]));
  return result;
}

console.log(palindromePairs(["abcd", "dcba", "lls", "s", "sssll"]));
