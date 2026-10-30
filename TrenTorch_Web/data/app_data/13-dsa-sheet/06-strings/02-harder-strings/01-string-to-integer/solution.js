// O(n) time, O(1) space
function myAtoi(s) {
  let i = 0;
  const n = s.length;
  while (i < n && s[i] === ' ') {
    i++;
  }
  let sign = 1;
  if (i < n && (s[i] === '+' || s[i] === '-')) {
    sign = s[i] === '-' ? -1 : 1;
    i++;
  }
  let value = 0;
  while (i < n && s[i] >= '0' && s[i] <= '9') {
    value = value * 10 + (s.charCodeAt(i) - 48);
    i++;
    if (value > 2 ** 31) {
      break;
    }
  }
  value *= sign;
  const INT_MIN = -(2 ** 31);
  const INT_MAX = 2 ** 31 - 1;
  if (value < INT_MIN) return INT_MIN;
  if (value > INT_MAX) return INT_MAX;
  return value;
}

console.log(myAtoi("42"));
