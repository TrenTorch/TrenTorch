function bitFlipsToConvert(a, b) {
  // O(k) time where k is number of differing bits (max 31), O(1) space
  let diff = a ^ b;
  let count = 0;
  while (diff !== 0) {
    diff &= diff - 1;
    count++;
  }
  return count;
}

console.log(bitFlipsToConvert(10, 7));
