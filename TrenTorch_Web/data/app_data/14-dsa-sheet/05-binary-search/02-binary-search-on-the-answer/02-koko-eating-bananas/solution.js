// O(n log M) time, O(1) space where M = max(piles)
function minEatingSpeed(piles, hours) {
  let lo = 1;
  let hi = Math.max(...piles);
  while (lo < hi) {
    const mid = Math.floor((lo + hi) / 2);
    let needed = 0;
    for (const p of piles) {
      needed += Math.ceil(p / mid);
    }
    if (needed <= hours) {
      hi = mid;
    } else {
      lo = mid + 1;
    }
  }
  return lo;
}

console.log(minEatingSpeed([3, 6, 7, 11], 8));
