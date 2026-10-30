// O(sqrt(n)) time, O(1) space
function countDivisors(n) {
  let count = 0;
  let d = 1;
  while (d * d <= n) {
    if (n % d === 0) {
      count += (d * d === n) ? 1 : 2;
    }
    d++;
  }
  return count;
}

console.log(countDivisors(36));
