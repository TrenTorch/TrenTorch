function shipCapacity(weights, days) {
  // O(n log S) time, O(1) space where S = sum(weights)
  let lo = Math.max(...weights);
  let hi = weights.reduce((a, b) => a + b, 0);
  while (lo < hi) {
    const mid = Math.floor((lo + hi) / 2);
    let needed = 1;
    let load = 0;
    for (const w of weights) {
      if (load + w > mid) {
        needed++;
        load = 0;
      }
      load += w;
    }
    if (needed <= days) {
      hi = mid;
    } else {
      lo = mid + 1;
    }
  }
  return lo;
}

console.log(shipCapacity([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5));
