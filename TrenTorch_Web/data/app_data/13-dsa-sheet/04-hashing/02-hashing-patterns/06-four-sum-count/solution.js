// O(n^2) time, O(n^2) space
function fourSumCount(a, b, c, d) {
  const sumMap = new Map();
  for (const x of a) {
    for (const y of b) {
      const s = x + y;
      sumMap.set(s, (sumMap.get(s) || 0) + 1);
    }
  }
  let count = 0;
  for (const z of c) {
    for (const w of d) {
      const target = -(z + w);
      count += sumMap.get(target) || 0;
    }
  }
  return count;
}

console.log(fourSumCount([1, 2], [-2, -1], [-1, 2], [0, 2]));
