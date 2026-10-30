// O(n) time, O(n) space
function runHitCounter(ops) {
  const window = [];
  let start = 0;
  const out = [];
  for (const op of ops) {
    const [kind, tStr] = op.split(' ');
    const t = parseInt(tStr, 10);
    if (kind === 'hit') {
      window.push(t);
    } else { // count
      while (start < window.length && window[start] <= t - 300) {
        start++;
      }
      out.push(window.length - start);
    }
  }
  return out;
}

console.log(runHitCounter(["hit 1", "hit 2", "hit 3", "count 4", "hit 300", "count 300", "count 301"]));
