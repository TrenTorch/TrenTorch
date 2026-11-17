// O(n * k) time, O(k) space
function maxProfitK(k, prices) {
  if (k === 0 || prices.length < 2) {
    return 0;
  }
  if (k >= Math.floor(prices.length / 2)) {
    let profit = 0;
    for (let i = 1; i < prices.length; i++) {
      const diff = prices[i] - prices[i - 1];
      if (diff > 0) profit += diff;
    }
    return profit;
  }
  const hold = new Array(k + 1).fill(-Infinity);
  const free = new Array(k + 1).fill(0);
  for (const p of prices) {
    for (let t = 1; t <= k; t++) {
      hold[t] = Math.max(hold[t], free[t - 1] - p);
      free[t] = Math.max(free[t], hold[t] + p);
    }
  }
  return free[k];
}

console.log(maxProfitK(2, [3, 2, 6, 5, 0, 3]));
