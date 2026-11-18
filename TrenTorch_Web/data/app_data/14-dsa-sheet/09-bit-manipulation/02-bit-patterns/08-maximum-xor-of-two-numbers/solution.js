// O(n) time, O(n) space
function maxXorPair(nums) {
  let best = 0;
  for (let bit = 29; bit >= 0; bit--) {
    const prefixes = new Set();
    for (const x of nums) {
      prefixes.add(x >> bit);
    }
    const candidate = (best << 1) | 1;
    best <<= 1;
    for (const p of prefixes) {
      if (prefixes.has(p ^ candidate)) {
        best = candidate;
        break;
      }
    }
  }
  return best;
}

console.log(maxXorPair([3, 10, 5, 25, 2, 8]));
