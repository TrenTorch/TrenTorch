// O(n log n) time, O(n) space
function largestNumber(nums) {
  const strings = nums.map(String);
  strings.sort((a, b) => {
    const ab = a + b;
    const ba = b + a;
    if (ab > ba) return -1;
    if (ab < ba) return 1;
    return 0;
  });
  const result = strings.join('');
  return result && result[0] !== '0' ? result : '0';
}

console.log(largestNumber([10, 2]));
