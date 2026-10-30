// O(1) time, O(1) space
function fewestNotes(amount) {
  let total = 0;
  const denominations = [2000, 500, 100, 50, 20, 10, 5, 2, 1];
  for (const value of denominations) {
    const count = Math.floor(amount / value);
    total += count;
    amount %= value;
  }
  return total;
}

console.log(fewestNotes(70));
