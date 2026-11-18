// O(n^2) time, O(n) space
function minCutPalindromes(s) {
  const n = s.length;
  if (n === 0) {
    return 0;
  }
  const cuts = Array.from({ length: n + 1 }, (_, i) => i - 1);
  for (let centre = 0; centre < n; centre++) {
    for (const [leftStart, rightStart] of [[centre, centre], [centre, centre + 1]]) {
      let left = leftStart;
      let right = rightStart;
      while (left >= 0 && right < n && s[left] === s[right]) {
        if (cuts[left] + 1 < cuts[right + 1]) {
          cuts[right + 1] = cuts[left] + 1;
        }
        left--;
        right++;
      }
    }
  }
  return cuts[n];
}

console.log(minCutPalindromes("aab"));
