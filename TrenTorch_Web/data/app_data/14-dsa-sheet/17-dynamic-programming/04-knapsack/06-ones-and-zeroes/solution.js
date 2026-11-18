// O(len(strs) * m * n) time, O(m * n) space
function findMaxForm(strs, m, n) {
  const best = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0));
  for (const s of strs) {
    let zeros = 0;
    for (const ch of s) {
      if (ch === '0') zeros++;
    }
    const ones = s.length - zeros;
    for (let z = m; z >= zeros; z--) {
      const row = best[z];
      const source = best[z - zeros];
      for (let o = n; o >= ones; o--) {
        const val = source[o - ones] + 1;
        if (val > row[o]) {
          row[o] = val;
        }
      }
    }
  }
  return best[m][n];
}

console.log(findMaxForm(["10", "0001", "111001", "1", "0"], 5, 3));
