// O(n) time, O(n) space
function longestConsecutive(nums) {
  const values = new Set(nums);
  let best = 0;
  for (const x of values) {
    if (!values.has(x - 1)) {
      let length = 1;
      while (values.has(x + length)) {
        length++;
      }
      if (length > best) best = length;
    }
  }
  return best;
}

console.log(longestConsecutive([100, 4, 200, 1, 3, 2]));
