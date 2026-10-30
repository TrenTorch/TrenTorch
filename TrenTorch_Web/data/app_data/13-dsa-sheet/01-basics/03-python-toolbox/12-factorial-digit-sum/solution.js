// O(n^2 log^2 n) time, O(n log n) space
function factorialDigitSum(n) {
  let f = 1n;
  for (let i = 2n; i <= BigInt(n); i++) {
    f *= i;
  }
  const s = f.toString();
  let sum = 0;
  for (let i = 0; i < s.length; i++) {
    sum += s.charCodeAt(i) - 48;
  }
  return sum;
}

console.log(factorialDigitSum(10));
