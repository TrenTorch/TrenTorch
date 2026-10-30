// O(n) time, O(n) space
function stockSpan(prices) {
  const out = [];
  const stack = [];
  for (let i = 0; i < prices.length; i++) {
    const p = prices[i];
    while (stack.length > 0 && prices[stack[stack.length - 1]] <= p) {
      stack.pop();
    }
    out.push(stack.length > 0 ? i - stack[stack.length - 1] : i + 1);
    stack.push(i);
  }
  return out;
}

console.log(stockSpan([100, 80, 60, 70, 60, 75, 85]));
