// O(n) time, O(1) space
function maxProfitMany(prices) {
  let profit = 0;
  for (let i = 1; i < prices.length; i++) {
    const diff = prices[i] - prices[i - 1];
    if (diff > 0) profit += diff;
  }
  return profit;
}

console.log(maxProfitMany([7, 1, 5, 3, 6, 4]));
