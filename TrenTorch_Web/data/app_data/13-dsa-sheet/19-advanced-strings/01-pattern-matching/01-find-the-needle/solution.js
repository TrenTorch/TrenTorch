// O(n + m) time, O(m) space
function findNeedle(haystack, needle) {
  if (needle.length === 0) return 0;
  const fail = new Array(needle.length).fill(0);
  let k = 0;
  for (let i = 1; i < needle.length; i++) {
    while (k > 0 && needle[i] !== needle[k]) {
      k = fail[k - 1];
    }
    if (needle[i] === needle[k]) {
      k++;
    }
    fail[i] = k;
  }
  k = 0;
  for (let i = 0; i < haystack.length; i++) {
    const ch = haystack[i];
    while (k > 0 && ch !== needle[k]) {
      k = fail[k - 1];
    }
    if (ch === needle[k]) {
      k++;
    }
    if (k === needle.length) {
      return i - k + 1;
    }
  }
  return -1;
}

console.log(findNeedle("sadbutsad", "sad"));
