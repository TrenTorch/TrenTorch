// O(n) time, O(1) space
function repeatingAndMissing(nums) {
  const n = nums.length;
  let sum = 0;
  let squareSum = 0;
  for (let i = 0; i < n; i++) {
    sum += nums[i];
    squareSum += nums[i] * nums[i];
  }
  const expectedSum = n * (n + 1) / 2;
  const expectedSquareSum = n * (n + 1) * (2 * n + 1) / 6;
  const diff = sum - expectedSum; // repeated - missing
  const squareDiff = squareSum - expectedSquareSum; // repeated^2 - missing^2
  const plus = squareDiff / diff; // repeated + missing
  const repeated = (plus + diff) / 2;
  const missing = (plus - diff) / 2;
  return [repeated, missing];
}

console.log(repeatingAndMissing([3, 1, 2, 5, 3]));
