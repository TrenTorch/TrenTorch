function calculateBrackets(s) {
  // O(n) time, O(n) space
  const stack = [];
  let result = 0;
  let num = 0;
  let sign = 1;
  for (const ch of s) {
    if (ch >= '0' && ch <= '9') {
      num = num * 10 + (ch.charCodeAt(0) - 48);
    } else if (ch === '+' || ch === '-') {
      result += sign * num;
      num = 0;
      sign = ch === '+' ? 1 : -1;
    } else if (ch === '(') {
      stack.push([result, sign]);
      result = 0;
      sign = 1;
    } else if (ch === ')') {
      result += sign * num;
      num = 0;
      const [savedResult, savedSign] = stack.pop();
      result = savedResult + savedSign * result;
    }
  }
  return result + sign * num;
}

console.log(calculateBrackets("(1+(4+5+2)-3)+(6+8)"));
