function removeDuplicateLetters(s) {
  // O(n) time, O(1) space (alphabet size fixed)
  const last = {};
  for (let i = 0; i < s.length; i++) {
    last[s[i]] = i;
  }
  const stack = [];
  const inStack = new Set();
  for (let i = 0; i < s.length; i++) {
    const ch = s[i];
    if (inStack.has(ch)) continue;
    while (stack.length > 0 && stack[stack.length - 1] > ch && last[stack[stack.length - 1]] > i) {
      inStack.delete(stack.pop());
    }
    stack.push(ch);
    inStack.add(ch);
  }
  return stack.join('');
}

console.log(removeDuplicateLetters("bcabc"));
