function runTimeMap(ops) {
  // O(n log m) time, O(n) space where n is number of ops, m is max sets per key
  const timesMap = new Map();
  const valuesMap = new Map();
  const out = [];

  function bisectRight(arr, x) {
    let lo = 0;
    let hi = arr.length;
    while (lo < hi) {
      const mid = (lo + hi) >> 1;
      if (arr[mid] <= x) lo = mid + 1;
      else hi = mid;
    }
    return lo;
  }

  for (const op of ops) {
    const parts = op.split(' ');
    if (parts[0] === 'set') {
      const key = parts[1];
      const value = parts[2];
      const t = parseInt(parts[3], 10);
      if (!timesMap.has(key)) {
        timesMap.set(key, []);
        valuesMap.set(key, []);
      }
      timesMap.get(key).push(t);
      valuesMap.get(key).push(value);
    } else { // get
      const key = parts[1];
      const t = parseInt(parts[2], 10);
      const times = timesMap.get(key) || [];
      const i = bisectRight(times, t);
      if (i > 0) {
        out.push(valuesMap.get(key)[i - 1]);
      } else {
        out.push('');
      }
    }
  }
  return out;
}

console.log(runTimeMap(["set love high 10", "get love 10", "get love 15", "set love low 20", "get love 15", "get love 25", "get love 5"]));
