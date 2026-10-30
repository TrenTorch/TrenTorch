// O(n log n) time, O(n) space
function fractionalKnapsack(items, capacity) {
  let total = 0;
  const sortedItems = items.slice().sort((a, b) => (b[0] / b[1]) - (a[0] / a[1]));
  for (const [value, weight] of sortedItems) {
    if (capacity === 0) break;
    const take = Math.min(weight, capacity);
    total += value * take / weight;
    capacity -= take;
  }
  return total;
}

console.log(fractionalKnapsack([[60, 10], [100, 20], [120, 30]], 50));
