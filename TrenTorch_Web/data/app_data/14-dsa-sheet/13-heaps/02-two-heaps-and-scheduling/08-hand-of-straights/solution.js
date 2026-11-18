// O(n log n) time, O(n) space
function isNStraightHand(hand, groupSize) {
  if (hand.length % groupSize !== 0) return false;
  const count = new Map();
  for (const x of hand) {
    count.set(x, (count.get(x) ?? 0) + 1);
  }
  const keys = Array.from(count.keys()).sort((a, b) => a - b);
  for (const start of keys) {
    const c = count.get(start);
    if (c > 0) {
      for (let x = start; x < start + groupSize; x++) {
        const cur = count.get(x) ?? 0;
        if (cur < c) return false;
        count.set(x, cur - c);
      }
    }
  }
  return true;
}

console.log(isNStraightHand([1, 2, 3, 6, 2, 3, 4, 7, 8], 3));
