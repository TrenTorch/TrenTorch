// O(1) time, O(1) space
function lowestSetBit(n) {
  const bigN = BigInt(n);
  const res = bigN & (-bigN);
  return res.toString();
}

console.log(lowestSetBit(12));
