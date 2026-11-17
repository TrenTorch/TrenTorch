// O(n) time, O(1) space
function majorityElement(nums) {
  let candidate = null;
  let count = 0;
  for (const x of nums) {
    if (count === 0) {
      candidate = x;
    }
    count += (x === candidate) ? 1 : -1;
  }
  if (candidate !== null && nums.filter(x => x === candidate).length > nums.length / 2) {
    return candidate;
  }
  return -1;
}

console.log(majorityElement([2, 2, 1, 1, 2, 2, 3]));
