// O(n + m) time, O(m) space
function countOverlapping(text, pattern) {
  const m = pattern.length;
  const fail = new Array(m).fill(0);
  let k = 0;
  for (let i = 1; i < m; i++) {
    while (k > 0 && pattern[i] !== pattern[k]) {
      k = fail[k - 1];
    }
    if (pattern[i] === pattern[k]) {
      k++;
    }
    fail[i] = k;
  }
  let count = 0;
  k = 0;
  for (const ch of text) {
    while (k > 0 && ch !== pattern[k]) {
      k = fail[k - 1];
    }
    if (ch === pattern[k]) {
      k++;
    }
    if (k === m) {
      count++;
      k = fail[k - 1];
    }
  }
  return count;
}

console.log(countOverlapping("aaaa", "aa"));
