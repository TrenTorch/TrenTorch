// O(n log n) time, O(n) space where n = a.length + b.length
function commonValues(a, b) {
  const setA = new Set(a);
  const setB = new Set(b);
  const intersection = [];
  for (const val of setA) {
    if (setB.has(val)) {
      intersection.push(val);
    }
  }
  return intersection.sort((x, y) => x - y);
}

console.log(commonValues([1, 2, 2, 3], [2, 2, 3, 4]));
