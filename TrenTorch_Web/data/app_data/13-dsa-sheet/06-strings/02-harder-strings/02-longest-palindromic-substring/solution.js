// O(n) time, O(n) space
function longestPalindromicSubstring(s) {
  const t = "#" + s.split("").join("#") + "#";
  const n = t.length;
  const radius = new Array(n).fill(0);
  let centre = 0;
  let right = 0;
  let bestLen = 0;
  let bestCentre = 0;
  for (let i = 0; i < n; i++) {
    if (i < right) {
      const mirror = 2 * centre - i;
      radius[i] = Math.min(right - i, radius[mirror]);
    }
    while (
      i - radius[i] - 1 >= 0 &&
      i + radius[i] + 1 < n &&
      t[i - radius[i] - 1] === t[i + radius[i] + 1]
    ) {
      radius[i]++;
    }
    if (i + radius[i] > right) {
      centre = i;
      right = i + radius[i];
    }
    if (radius[i] > bestLen) {
      bestLen = radius[i];
      bestCentre = i;
    }
  }
  const start = Math.floor((bestCentre - bestLen) / 2);
  return s.substring(start, start + bestLen);
}

console.log(longestPalindromicSubstring("babad"));
