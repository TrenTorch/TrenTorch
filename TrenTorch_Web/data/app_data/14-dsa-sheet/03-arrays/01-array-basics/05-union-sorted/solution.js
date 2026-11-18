// O(n + m) time, O(n + m) space
function unionSorted(a, b) {
  const out = [];
  let i = 0, j = 0;
  while (i < a.length || j < b.length) {
    let x;
    if (j === b.length || (i < a.length && a[i] <= b[j])) {
      x = a[i];
      i++;
    } else {
      x = b[j];
      j++;
    }
    if (out.length === 0 || out[out.length - 1] !== x) {
      out.push(x);
    }
  }
  return out;
}

console.log(unionSorted([1, 2, 2, 4], [2, 3, 4, 5]));
