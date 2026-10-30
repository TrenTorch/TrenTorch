// O(n * capacity) time, O(capacity) space
function unboundedKnapsack(weights, values, capacity) {
  const best = new Array(capacity + 1).fill(0);
  for (let i = 0; i < weights.length; i++) {
    const weight = weights[i];
    const value = values[i];
    for (let w = weight; w <= capacity; w++) {
      const candidate = best[w - weight] + value;
      if (candidate > best[w]) {
        best[w] = candidate;
      }
    }
  }
  return best[capacity];
}

console.log(unboundedKnapsack([1, 3, 4], [15, 50, 60], 8));
