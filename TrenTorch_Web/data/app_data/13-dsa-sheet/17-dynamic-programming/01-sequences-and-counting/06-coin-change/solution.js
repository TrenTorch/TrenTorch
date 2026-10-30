// O(amount * n) time, O(amount) space where n = coins.length
function coinChange(coins, amount) {
  const inf = Infinity;
  const best = new Array(amount + 1).fill(inf);
  best[0] = 0;
  
  for (let a = 1; a <= amount; a++) {
    for (const c of coins) {
      if (c <= a && best[a - c] + 1 < best[a]) {
        best[a] = best[a - c] + 1;
      }
    }
  }
  
  return best[amount] !== inf ? best[amount] : -1;
}

console.log(coinChange([1, 2, 5], 11));
