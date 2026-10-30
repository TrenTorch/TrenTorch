// O(1) time, O(1) space
function countDoublingSteps(n) {
  const bn = BigInt(n);
  if (bn <= 1n) return 0;
  const bits = (bn - 1n).toString(2).length;
  return Number(bits);
}

console.log(countDoublingSteps(8));
