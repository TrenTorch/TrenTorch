// O(1) time, O(1) space
function swapOddEvenBits(n) {
  const evenMask = 0x55555555;
  const oddMask = 0xAAAAAAAA;
  const even = (n & evenMask) << 1;
  const odd = (n & oddMask) >>> 1;
  return (even | odd) >>> 0;
}

console.log(swapOddEvenBits(10));
