// O(log(min(m, n))) time, O(1) space
function medianTwoSorted(a, b) {
  if (a.length > b.length) {
    [a, b] = [b, a];
  }
  const m = a.length;
  const n = b.length;
  const half = Math.floor((m + n + 1) / 2);
  let lo = 0;
  let hi = m;
  while (lo <= hi) {
    const i = Math.floor((lo + hi) / 2);
    const j = half - i;
    const aLeft = i > 0 ? a[i - 1] : -Infinity;
    const aRight = i < m ? a[i] : Infinity;
    const bLeft = j > 0 ? b[j - 1] : -Infinity;
    const bRight = j < n ? b[j] : Infinity;
    if (aLeft <= bRight && bLeft <= aRight) {
      if ((m + n) % 2 === 1) {
        return Math.max(aLeft, bLeft);
      }
      return (Math.max(aLeft, bLeft) + Math.min(aRight, bRight)) / 2;
    }
    if (aLeft > bRight) {
      hi = i - 1;
    } else {
      lo = i + 1;
    }
  }
}

console.log(medianTwoSorted([1, 3], [2]));
