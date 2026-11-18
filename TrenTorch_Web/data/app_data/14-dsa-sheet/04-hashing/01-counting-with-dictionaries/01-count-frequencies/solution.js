// O(n + m) time, O(n) space
function countFrequencies(nums, queries) {
  const freq = new Map();
  for (const num of nums) {
    freq.set(num, (freq.get(num) ?? 0) + 1);
  }
  const result = [];
  for (const q of queries) {
    result.push(freq.get(q) ?? 0);
  }
  return result;
}

console.log(countFrequencies([1, 2, 2, 3, 3, 3], [3, 2, 5]));
