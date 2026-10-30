// O(n) time, O(1) space
function maxPoints(points, k) {
  const n = points.length;
  const size = n - k;
  let window = 0;
  for (let i = 0; i < size; i++) {
    window += points[i];
  }
  let smallest = window;
  for (let i = size; i < n; i++) {
    window += points[i] - points[i - size];
    if (window < smallest) smallest = window;
  }
  const total = points.reduce((sum, val) => sum + val, 0);
  return total - smallest;
}

console.log(maxPoints([1, 2, 3, 4, 5, 6, 1], 3));
