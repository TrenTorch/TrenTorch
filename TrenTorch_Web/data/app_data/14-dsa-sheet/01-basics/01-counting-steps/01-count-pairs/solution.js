// O(1) time, O(1) space
function countPairs(n) {
  const N = BigInt(n);
  return (N * (N - 1n) / 2n).toString();
}

console.log(countPairs(4));
