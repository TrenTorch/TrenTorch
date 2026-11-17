// O(n) time, O(n) space
function evaluateRpn(tokens) {
  const stack = [];
  for (const token of tokens) {
    if (token === "+" || token === "-" || token === "*" || token === "/") {
      const b = stack.pop();
      const a = stack.pop();
      let result;
      if (token === "+") {
        result = a + b;
      } else if (token === "-") {
        result = a - b;
      } else if (token === "*") {
        result = a * b;
      } else {
        result = Math.trunc(a / b);
      }
      stack.push(result);
    } else {
      stack.push(parseInt(token, 10));
    }
  }
  return stack[0];
}

console.log(evaluateRpn(["2", "1", "+", "3", "*"]));
