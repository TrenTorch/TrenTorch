// O(n) time, O(n) space
function queueWithTwoStacks(ops) {
  const inbox = [];
  const outbox = [];
  const out = [];

  function move() {
    if (outbox.length === 0) {
      while (inbox.length > 0) {
        outbox.push(inbox.pop());
      }
    }
  }

  for (const op of ops) {
    if (op.startsWith("push")) {
      const parts = op.split(" ");
      inbox.push(parseInt(parts[1], 10));
    } else if (op === "pop") {
      move();
      out.push(outbox.pop());
    } else if (op === "peek") {
      move();
      out.push(outbox[outbox.length - 1]);
    } else { // empty
      out.push((inbox.length > 0 || outbox.length > 0) ? 0 : 1);
    }
  }
  return out;
}

console.log(queueWithTwoStacks(["push 1", "push 2", "peek", "pop", "empty"]));
