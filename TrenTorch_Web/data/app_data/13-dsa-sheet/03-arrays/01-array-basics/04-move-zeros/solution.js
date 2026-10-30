// O(n) time, O(n) space
function moveZeros(nums) {
  const nonZero = nums.filter(x => x !== 0);
  const zeroCount = nums.length - nonZero.length;
  return nonZero.concat(Array(zeroCount).fill(0));
}

console.log(moveZeros([0, 1, 0, 3, 12]));
