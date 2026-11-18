// O(n log n) time, O(n) space
function aggressiveCows(stalls, cows) {
  const s = [...stalls].sort((a, b) => a - b);

  function canPlace(distance) {
    let placed = 1;
    let last = s[0];
    for (let i = 1; i < s.length; i++) {
      if (s[i] - last >= distance) {
        placed++;
        last = s[i];
      }
    }
    return placed >= cows;
  }

  let lo = 1;
  let hi = s[s.length - 1] - s[0];
  while (lo < hi) {
    const mid = Math.floor((lo + hi + 1) / 2);
    if (canPlace(mid)) {
      lo = mid;
    } else {
      hi = mid - 1;
    }
  }
  return lo;
}

console.log(aggressiveCows([1, 2, 4, 8, 9], 3));
