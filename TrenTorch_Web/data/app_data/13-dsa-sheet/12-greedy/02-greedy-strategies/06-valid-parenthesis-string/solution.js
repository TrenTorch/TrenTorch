// O(n) time, O(1) space
function checkValidString(s) {
  let lo = 0, hi = 0;
  for (const ch of s) {
    if (ch === '(') {
      lo += 1;
      hi += 1;
    } else if (ch === ')') {
      lo -= 1;
      hi -= 1;
    } else { // '*'
      lo -= 1;
      hi += 1;
    }
    if (hi < 0) return false;
    if (lo < 0) lo = 0;
  }
  return lo === 0;
}

console.log(checkValidString("(*)"));
