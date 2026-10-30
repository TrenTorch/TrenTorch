// O(2^{n/2}) time, O(2^{n/2}) space
function _sumsBySize(values) {
  const states = new Map();
  const makeKey = (size, total) => `${size},${total}`;
  states.set(makeKey(0, 0), 1);
  for (const v of values) {
    const snapshot = Array.from(states.entries());
    for (const [key, ways] of snapshot) {
      const [sizeStr, totalStr] = key.split(',');
      const size = Number(sizeStr);
      const total = Number(totalStr);
      const newKey = makeKey(size + 1, total + v);
      const prev = states.get(newKey) || 0;
      states.set(newKey, prev + ways);
    }
  }
  return states;
}

/**
 * Count the ways to choose exactly `k` positions from `nums` so that the chosen values add up to `target`.
 * @param {number[]} nums
 * @param {number} k
 * @param {number} target
 * @returns {number}
 */
function countSubsetSums(nums, k, target) {
  const half = Math.floor(nums.length / 2);
  const left = _sumsBySize(nums.slice(0, half));
  const right = _sumsBySize(nums.slice(half));
  const makeKey = (size, total) => `${size},${total}`;
  let count = 0;
  for (const [key, ways] of right.entries()) {
    const [sizeStr, totalStr] = key.split(',');
    const size = Number(sizeStr);
    const total = Number(totalStr);
    const complementKey = makeKey(k - size, target - total);
    const leftWays = left.get(complementKey) || 0;
    count += ways * leftWays;
  }
  return count;
}

console.log(countSubsetSums([1, 2, 3, 4], 2, 5));
