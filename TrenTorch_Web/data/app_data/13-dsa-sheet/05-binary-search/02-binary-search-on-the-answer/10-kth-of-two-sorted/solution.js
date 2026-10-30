// O(log(min(m,n))) time, O(1) space
function kthOfTwoSorted(a, b, k) {
  if (a.length > b.length) {
    [a, b] = [b, a];
  }
  const m = a.length;
  const n = b.length;
  let lo = Math.max(0, k - n);
  let hi = Math.min(k, m);
  while (lo <= hi) {
    const i = (lo + hi) >> 1;
    const j = k - i;
    const aLeft = i > 0 ? a[i - 1] : -Infinity;
    const aRight = i < m ? a[i] : Infinity;
    const bLeft = j > 0 ? b[j - 1] : -Infinity;
    const bRight = j < n ? b[j] : Infinity;
    if (aLeft <= bRight && bLeft <= aRight) {
      return Math.max(aLeft, bLeft);
    }
    if (aLeft > bRight) {
      hi = i - 1;
    } else {
      lo = i + 1;
    }
  }
}

console.log(kthOfTwoSorted([2, 3, 6, 7, 9], [1, 4, 8, 10], 5));
