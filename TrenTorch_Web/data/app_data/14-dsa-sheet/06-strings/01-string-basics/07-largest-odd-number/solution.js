// O(n) time, O(1) space
function largestOddNumber(num) {
  for (let i = num.length - 1; i >= 0; i--) {
    const ch = num[i];
    if (ch === '1' || ch === '3' || ch === '5' || ch === '7' || ch === '9') {
      return num.slice(0, i + 1);
    }
  }
  return "";
}

console.log(largestOddNumber("52"));
