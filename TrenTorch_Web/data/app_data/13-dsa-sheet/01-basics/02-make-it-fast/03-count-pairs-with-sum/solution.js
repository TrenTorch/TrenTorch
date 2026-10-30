// O(n) time, O(n) space
function countPairsWithSum(nums, target) {
  const seen = new Map();
  let count = 0;
  for (const x of nums) {
    const need = target - x;
    const have = seen.get(need) || 0;
    count += have;
    seen.set(x, (seen.get(x) || 0) + 1);
  }
  return count;
}

console.log(countPairsWithSum([1, 2, 3, 4, 3], 6));
