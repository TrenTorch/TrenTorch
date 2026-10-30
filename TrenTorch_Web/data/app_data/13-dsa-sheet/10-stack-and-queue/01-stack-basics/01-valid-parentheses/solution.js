// O(n) time, O(n) space
function validBrackets(s) {
  const match = { ")": "(", "]": "[", "}": "{" };
  const stack = [];
  for (const ch of s) {
    if (ch in match) {
      if (stack.length === 0 || stack.pop() !== match[ch]) {
        return false;
      }
    } else {
      stack.push(ch);
    }
  }
  return stack.length === 0;
}

console.log(validBrackets("()[]{}"));
