function sumDivisorCounts(n) {
  // O(sqrt(n)) time, O(1) space
  const r = Math.floor(Math.sqrt(n));
  let sum = 0;
  for (let j = 1; j <= r; j++) {
    sum += Math.floor(n / j);
  }
  return 2 * sum - r * r;
}

console.log(sumDivisorCounts(5));
