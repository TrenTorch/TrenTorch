// O(n) time, O(1) space
function longestValidParentheses(s) {
  let best = 0;

  // forward pass
  let left = 0, right = 0;
  const openerForward = '(';
  for (let i = 0; i < s.length; i++) {
    const ch = s[i];
    if (ch === openerForward) {
      left++;
    } else {
      right++;
    }
    if (left === right) {
      best = Math.max(best, 2 * left);
    } else if (right > left) {
      left = right = 0;
    }
  }

  // backward pass
  left = right = 0;
  const openerBackward = ')';
  for (let i = s.length - 1; i >= 0; i--) {
    const ch = s[i];
    if (ch === openerBackward) {
      left++;
    } else {
      right++;
    }
    if (left === right) {
      best = Math.max(best, 2 * left);
    } else if (right > left) {
      left = right = 0;
    }
  }

  return best;
}

console.log(longestValidParentheses(")()())"));
