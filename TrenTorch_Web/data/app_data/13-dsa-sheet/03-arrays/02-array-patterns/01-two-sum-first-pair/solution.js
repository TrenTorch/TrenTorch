// O(n) time, O(n) space
function twoSumFirstPair(nums, target) {
  const first = new Map();
  let best = null;
  for (let j = 0; j < nums.length; j++) {
    const x = nums[j];
    const complement = target - x;
    if (first.has(complement)) {
      const i = first.get(complement);
      if (best === null || i < best[0] || (i === best[0] && j < best[1])) {
        best = [i, j];
      }
    }
    if (!first.has(x)) {
      first.set(x, j);
    }
  }
  return best === null ? [-1, -1] : best;
}

console.log(twoSumFirstPair([1, 6, 5, 3, 8], 9));
