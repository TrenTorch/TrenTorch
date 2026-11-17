// O(1) time, O(1) space
function countHalvingSteps(n) {
  return Math.floor(Math.log2(n));
}

console.log(countHalvingSteps(8));
