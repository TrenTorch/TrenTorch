// O(n log D) time, O(1) space
function minDaysBouquets(bloom, m, k) {
  if (m * k > bloom.length) return -1;

  function possible(day) {
    let bouquets = 0;
    let run = 0;
    for (const b of bloom) {
      if (b <= day) {
        run++;
        if (run === k) {
          bouquets++;
          run = 0;
        }
      } else {
        run = 0;
      }
    }
    return bouquets >= m;
  }

  let lo = Math.min(...bloom);
  let hi = Math.max(...bloom);
  while (lo < hi) {
    const mid = Math.floor((lo + hi) / 2);
    if (possible(mid)) {
      hi = mid;
    } else {
      lo = mid + 1;
    }
  }
  return lo;
}

console.log(minDaysBouquets([1, 10, 3, 10, 2], 3, 1));
