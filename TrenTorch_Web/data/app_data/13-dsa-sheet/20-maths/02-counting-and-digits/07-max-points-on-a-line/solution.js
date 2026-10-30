// O(n^2) time, O(n) space
function maxPoints(points) {
  const n = points.length;
  if (n <= 2) return n;
  let best = 2;
  for (let i = 0; i < n; i++) {
    const slopes = new Map();
    const x0 = points[i][0];
    const y0 = points[i][1];
    for (let j = i + 1; j < n; j++) {
      let dx = points[j][0] - x0;
      let dy = points[j][1] - y0;
      const g = gcd(dx, dy);
      dx /= g;
      dy /= g;
      dx = Math.trunc(dx);
      dy = Math.trunc(dy);
      if (dx < 0 || (dx === 0 && dy < 0)) {
        dx = -dx;
        dy = -dy;
      }
      const key = dx + ',' + dy;
      slopes.set(key, (slopes.get(key) || 0) + 1);
    }
    if (slopes.size > 0) {
      const maxCount = Math.max(...slopes.values());
      best = Math.max(best, maxCount + 1);
    }
  }
  return best;
}

function gcd(a, b) {
  a = Math.abs(a);
  b = Math.abs(b);
  while (b !== 0) {
    const t = b;
    b = a % b;
    a = t;
  }
  return a;
}

console.log(maxPoints([[1, 1], [2, 2], [3, 3]]));
