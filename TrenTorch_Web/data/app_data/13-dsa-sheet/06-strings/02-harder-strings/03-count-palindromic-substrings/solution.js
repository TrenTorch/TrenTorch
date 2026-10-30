// O(n) time, O(n) space
function countPalindromicSubstrings(s) {
  const t = "#" + s.split("").join("#") + "#";
  const n = t.length;
  const radius = new Array(n).fill(0);
  let centre = 0;
  let right = 0;
  for (let i = 0; i < n; i++) {
    if (i < right) {
      radius[i] = Math.min(right - i, radius[2 * centre - i]);
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
  }
  let total = 0;
  for (const r of radius) {
    total += Math.floor((r + 1) / 2);
  }
  return total;
}

console.log(countPalindromicSubstrings("abc"));
