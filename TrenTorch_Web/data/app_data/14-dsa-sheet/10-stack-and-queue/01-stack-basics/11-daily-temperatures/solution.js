// O(n) time, O(n) space
function dailyTemperatures(temps) {
  const out = new Array(temps.length).fill(0);
  const stack = [];
  for (let i = 0; i < temps.length; i++) {
    const t = temps[i];
    while (stack.length && temps[stack[stack.length - 1]] < t) {
      const j = stack.pop();
      out[j] = i - j;
    }
    stack.push(i);
  }
  return out;
}

console.log(dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]));
