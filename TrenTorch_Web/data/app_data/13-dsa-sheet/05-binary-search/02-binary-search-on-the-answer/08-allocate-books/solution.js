// O(n log S) time, O(1) space where S is sum of pages
function allocateBooks(pages, students) {
  if (students > pages.length) return -1;
  let lo = Math.max(...pages);
  let hi = pages.reduce((a, b) => a + b, 0);
  while (lo < hi) {
    const mid = Math.floor((lo + hi) / 2);
    let needed = 1;
    let load = 0;
    for (const p of pages) {
      if (load + p > mid) {
        needed++;
        load = 0;
      }
      load += p;
    }
    if (needed <= students) {
      hi = mid;
    } else {
      lo = mid + 1;
    }
  }
  return lo;
}

console.log(allocateBooks([12, 34, 67, 90], 2));
