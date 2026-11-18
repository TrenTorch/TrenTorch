// O(log m) time, O(1) space
function modInverse(a, m) {
  if (m === 1) {
    return 0;
  }
  let oldR = a % m;
  let r = m;
  let oldX = 1;
  let x = 0;
  while (r !== 0) {
    const q = Math.floor(oldR / r);
    [oldR, r] = [r, oldR - q * r];
    [oldX, x] = [x, oldX - q * x];
  }
  return oldR === 1 ? ((oldX % m) + m) % m : -1;
}

console.log(modInverse(3, 11));
