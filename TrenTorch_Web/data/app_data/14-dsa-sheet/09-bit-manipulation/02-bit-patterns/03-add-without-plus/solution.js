// O(1) time (≤32 iterations), O(1) space
function bitAdd(a, b) {
  const mask = 0xFFFFFFFF >>> 0; // ensure unsigned 32‑bit mask
  let x = a >>> 0; // convert to unsigned 32‑bit
  let y = b >>> 0;
  while (y !== 0) {
    const sum = (x ^ y) >>> 0;
    const carry = ((x & y) << 1) >>> 0;
    x = sum;
    y = carry;
  }
  // convert unsigned result to signed 32‑bit integer
  return (x & 0x80000000) ? x - 0x100000000 : x;
}

console.log(bitAdd(1, 2));
