// O(amount * n) time, O(amount) space
function countChange(amount, coins) {
  const MOD = 1000000007;
  const ways = new Array(amount + 1).fill(0);
  ways[0] = 1;
  for (const c of coins) {
    for (let a = c; a <= amount; a++) {
      ways[a] = (ways[a] + ways[a - c]) % MOD;
    }
  }
  return ways[amount];
}

console.log(countChange(5, [1, 2, 5]));
