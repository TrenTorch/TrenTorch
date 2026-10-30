// O(n) time, O(n) space
function minStack(ops) {
  const values = [];
  const mins = [];
  const out = [];
  for (const op of ops) {
    if (op.startsWith("push")) {
      const x = parseInt(op.split(" ")[1], 10);
      values.push(x);
      mins.push(mins.length === 0 ? x : Math.min(x, mins[mins.length - 1]));
    } else if (op === "pop") {
      values.pop();
      mins.pop();
    } else if (op === "top") {
      out.push(values[values.length - 1]);
    } else { // get_min
      out.push(mins[mins.length - 1]);
    }
  }
  return out;
}

console.log(minStack(["push 5", "push 3", "get_min", "pop", "top", "get_min"]));
