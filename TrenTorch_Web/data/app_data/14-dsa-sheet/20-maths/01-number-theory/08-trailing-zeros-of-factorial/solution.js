// O(log n) time, O(1) space
function trailingZeros(n) {
  let count = 0;
  while (n) {
    n = Math.floor(n / 5);
    count += n;
  }
  return count;
}

console.log(trailingZeros(25));
