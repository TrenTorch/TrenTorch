// O(n log n) time, O(n) space
function maxJobProfit(jobs) {
  const n = jobs.length;
  if (n === 0) return 0;

  // Determine the effective time limit
  let maxDeadline = 0;
  for (let i = 0; i < n; i++) {
    if (jobs[i][0] > maxDeadline) maxDeadline = jobs[i][0];
  }
  const limit = Math.min(maxDeadline, n);

  // Disjoint set (union-find) for available slots
  const parent = new Array(limit + 1);
  for (let i = 0; i <= limit; i++) parent[i] = i;

  function find(t) {
    while (parent[t] !== t) {
      parent[t] = parent[parent[t]];
      t = parent[t];
    }
    return t;
  }

  // Sort jobs by descending profit
  jobs.sort((a, b) => b[1] - a[1]);

  let total = 0;
  for (let i = 0; i < n; i++) {
    const deadline = jobs[i][0];
    const profit = jobs[i][1];
    const slot = find(Math.min(deadline, limit));
    if (slot > 0) {
      parent[slot] = slot - 1; // occupy this slot
      total += profit;
    }
  }
  return total;
}

console.log(maxJobProfit([[4, 20], [1, 10], [1, 40], [1, 30]]));
