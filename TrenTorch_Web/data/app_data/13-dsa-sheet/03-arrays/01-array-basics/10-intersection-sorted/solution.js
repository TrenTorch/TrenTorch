// O(n + m) time, O(min(n, m)) space
function intersectionSorted(a, b) {
  const out = [];
  let i = 0, j = 0;
  while (i < a.length && j < b.length) {
    if (a[i] === b[j]) {
      out.push(a[i]);
      i++;
      j++;
    } else if (a[i] < b[j]) {
      i++;
    } else {
      j++;
    }
  }
  return out;
}

console.log(intersectionSorted([1, 2, 2, 3], [2, 2, 2, 4]));
