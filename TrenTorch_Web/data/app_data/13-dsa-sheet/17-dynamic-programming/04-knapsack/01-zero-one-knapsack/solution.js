// O(n * capacity) time, O(capacity) space
function knapsack(weights, values, capacity) {
  const best = new Array(capacity + 1).fill(0);
  for (let i = 0; i < weights.length; i++) {
    const weight = weights[i];
    const value = values[i];
    for (let w = capacity; w >= weight; w--) {
      const candidate = best[w - weight] + value;
      if (candidate > best[w]) {
        best[w] = candidate;
      }
    }
  }
  return best[capacity];
}

console.log(knapsack([1, 3, 4, 5], [1, 4, 5, 7], 7));
