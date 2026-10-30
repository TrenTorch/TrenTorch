// O(√n) time, O(1) space
function countDivisorSteps(n) {
  let total = 0;
  let i = 1;
  while (i <= n) {
    const q = Math.floor(n / i);
    const j = Math.floor(n / q);
    total += q * (j - i + 1);
    i = j + 1;
  }
  return total;
}

console.log(countDivisorSteps(5));
