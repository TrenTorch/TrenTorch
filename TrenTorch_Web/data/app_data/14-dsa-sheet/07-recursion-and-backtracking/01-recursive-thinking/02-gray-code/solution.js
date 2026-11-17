// O(2^n) time, O(2^n) space
function grayCode(n) {
  const size = 1 << n;
  const result = new Array(size);
  for (let i = 0; i < size; i++) {
    result[i] = i ^ (i >> 1);
  }
  return result;
}

console.log(grayCode(2));
