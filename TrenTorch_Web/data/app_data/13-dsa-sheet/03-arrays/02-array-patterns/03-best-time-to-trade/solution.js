// O(n) time, O(1) space
function stockBestProfit(prices) {
  let best = 0;
  let lowest = null;
  for (const price of prices) {
    if (lowest !== null) {
      best = Math.max(best, price - lowest);
      lowest = Math.min(lowest, price);
    } else {
      lowest = price;
    }
  }
  return best;
}

console.log(stockBestProfit([7, 1, 5, 3, 6, 4]));
