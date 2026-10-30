// O(n + m) time, O(n) space
function rangeSums(nums, queries) {
  const prefix = new Array(nums.length + 1);
  prefix[0] = 0;
  for (let i = 0; i < nums.length; i++) {
    prefix[i + 1] = prefix[i] + nums[i];
  }
  return queries.map(([left, right]) => prefix[right + 1] - prefix[left]);
}

console.log(rangeSums([1, 2, 3, 4, 5], [[0, 4], [1, 3], [2, 2]]));
