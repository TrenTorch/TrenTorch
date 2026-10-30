// O(m log n) time, O(1) space
function nthRoot(n, m) {
  let lo = 1;
  let hi = n;
  while (lo <= hi) {
    const mid = Math.floor((lo + hi) / 2);
    let power = 1;
    for (let i = 0; i < m; i++) {
      power *= mid;
      if (power > n) break;
    }
    if (power === n) {
      return mid;
    }
    if (power < n) {
      lo = mid + 1;
    } else {
      hi = mid - 1;
    }
  }
  return -1;
}

console.log(nthRoot(27, 3));
