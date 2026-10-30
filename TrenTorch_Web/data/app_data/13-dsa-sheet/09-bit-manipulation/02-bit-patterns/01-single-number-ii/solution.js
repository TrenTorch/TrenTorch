// O(n) time, O(1) space
function singleNumberIi(nums) {
  let ones = 0, twos = 0;
  for (let x of nums) {
    ones = (ones ^ x) & ~twos;
    twos = (twos ^ x) & ~ones;
  }
  return ones;
}

console.log(singleNumberIi([2, 2, 3, 2]));
