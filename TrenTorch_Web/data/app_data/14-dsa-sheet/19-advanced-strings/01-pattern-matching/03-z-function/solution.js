// O(n) time, O(n) space
function zFunction(s) {
  const n = s.length;
  const z = new Array(n).fill(0);
  let left = 0, right = 0;
  for (let i = 1; i < n; i++) {
    if (i < right) {
      z[i] = Math.min(right - i, z[i - left]);
    }
    while (i + z[i] < n && s[z[i]] === s[i + z[i]]) {
      z[i]++;
    }
    if (i + z[i] > right) {
      left = i;
      right = i + z[i];
    }
  }
  return z;
}

console.log(zFunction("aabxaab"));
