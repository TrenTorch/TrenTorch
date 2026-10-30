// O(n) time, O(1) space
function singleNumber(nums) {
  return nums.reduce((acc, num) => acc ^ num, 0);
}

console.log(singleNumber([4, 1, 2, 1, 2]));
