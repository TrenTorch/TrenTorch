// O(n) time, O(n) space
function smallestRotation(s) {
  const n = s.length;
  if (n === 0) {
    return "";
  }
  const s2 = s + s;
  let i = 0, j = 1, k = 0;
  while (i < n && j < n && k < n) {
    const a = s2[i + k];
    const b = s2[j + k];
    if (a === b) {
      k++;
      continue;
    }
    if (a > b) {
      i += k + 1;
    } else {
      j += k + 1;
    }
    if (i === j) {
      j++;
    }
    k = 0;
  }
  const start = Math.min(i, j);
  return s2.substring(start, start + n);
}

console.log(smallestRotation("bca"));
