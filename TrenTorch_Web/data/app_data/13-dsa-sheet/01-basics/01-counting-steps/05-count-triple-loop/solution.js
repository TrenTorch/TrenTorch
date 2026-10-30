// O(1) time, O(1) space
function countTripleLoop(n) {
  return (n * (n + 1) * (n + 2)) / 6;
}

console.log(countTripleLoop(3));
