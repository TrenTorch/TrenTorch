// O(n) time, O(n) space
function removeAdjacentDuplicates(s) {
  const stack = [];
  for (let i = 0; i < s.length; i++) {
    const ch = s[i];
    if (stack.length && stack[stack.length - 1] === ch) {
      stack.pop();
    } else {
      stack.push(ch);
    }
  }
  return stack.join('');
}

console.log(removeAdjacentDuplicates("abbaca"));
