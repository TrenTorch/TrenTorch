// Average O(n) time, O(n) space (same as Python reference)
function compareKeys(a, b) {
  if (a[0] !== b[0]) return a[0] - b[0];
  if (a[1] !== b[1]) return a[1] - b[1];
  return a[2] - b[2];
}

function kClosest(points, k) {
  if (k <= 0) return [];
  let pool = points.map(p => {
    const x = p[0];
    const y = p[1];
    const dist = x * x + y * y;
    return { key: [dist, x, y], point: p };
  });

  if (k < pool.length) {
    const chosen = [];
    let need = k;
    while (need > 0) {
      const pivot = pool[Math.floor(Math.random() * pool.length)].key;
      const less = [];
      const equal = [];
      const greater = [];
      for (const item of pool) {
        const cmp = compareKeys(item.key, pivot);
        if (cmp < 0) less.push(item);
        else if (cmp === 0) equal.push(item);
        else greater.push(item);
      }
      if (need <= less.length) {
        pool = less;
      } else if (need <= less.length + equal.length) {
        chosen.push(...less);
        chosen.push(...equal.slice(0, need - less.length));
        need = 0;
      } else {
        chosen.push(...less);
        chosen.push(...equal);
        need -= less.length + equal.length;
        pool = greater;
      }
    }
    pool = chosen;
  }

  pool.sort((a, b) => compareKeys(a.key, b.key));
  return pool.map(item => item.point);
}

console.log(kClosest([[1, 3], [-2, 2]], 1));
