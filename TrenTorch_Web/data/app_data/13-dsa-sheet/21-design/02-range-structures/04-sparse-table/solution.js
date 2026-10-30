// O(n log n) time, O(n log n) space
function rangeMinimums(nums, queries) {
  const n = nums.length;
  // Build sparse table
  const table = [nums.slice()]; // level 0
  let k = 1;
  while ((1 << k) <= n) {
    const prev = table[k - 1];
    const half = 1 << (k - 1);
    const len = n - (1 << k) + 1;
    const curr = new Array(len);
    for (let i = 0; i < len; i++) {
      curr[i] = Math.min(prev[i], prev[i + half]);
    }
    table.push(curr);
    k++;
  }
  // Precompute floor(log2) for 1..n
  const log2 = new Array(n + 1);
  log2[1] = 0;
  for (let i = 2; i <= n; i++) {
    log2[i] = log2[i >> 1] + 1;
  }
  const out = [];
  for (const [left, right] of queries) {
    const len = right - left + 1;
    const level = log2[len];
    const row = table[level];
    const offset = 1 << level;
    out.push(Math.min(row[left], row[right - offset + 1]));
  }
  return out;
}

console.log(rangeMinimums([5, 2, 8, 1, 9], [[0, 4], [1, 2], [2, 2]]));
