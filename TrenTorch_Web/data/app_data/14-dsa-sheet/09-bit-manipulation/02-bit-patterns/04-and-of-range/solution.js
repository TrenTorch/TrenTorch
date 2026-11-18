// O(1) time, O(1) space
function andOfRange(left, right) {
  let xor = left ^ right;
  let shift = 0;
  while (xor > 0) {
    shift++;
    xor >>>= 1;
  }
  return (left >>> shift) << shift;
}

console.log(andOfRange(5, 7));
