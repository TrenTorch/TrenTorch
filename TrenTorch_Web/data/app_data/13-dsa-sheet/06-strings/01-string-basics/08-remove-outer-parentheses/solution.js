// O(n) time, O(n) space
function removeOuterParentheses(s) {
  const out = [];
  let depth = 0;
  for (const ch of s) {
    if (ch === '(') {
      if (depth > 0) out.push(ch);
      depth++;
    } else {
      depth--;
      if (depth > 0) out.push(ch);
    }
  }
  return out.join('');
}

console.log(removeOuterParentheses("(()())(())"));
