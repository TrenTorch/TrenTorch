// O(d) time, O(d) space where d = number of digits
function monotoneIncreasingDigits(n) {
  const digits = String(n).split('');
  let mark = digits.length;
  for (let i = digits.length - 1; i > 0; i--) {
    if (digits[i - 1] > digits[i]) {
      digits[i - 1] = String(Number(digits[i - 1]) - 1);
      mark = i;
    }
  }
  for (let i = mark; i < digits.length; i++) {
    digits[i] = '9';
  }
  return Number(digits.join(''));
}

console.log(monotoneIncreasingDigits(332));
