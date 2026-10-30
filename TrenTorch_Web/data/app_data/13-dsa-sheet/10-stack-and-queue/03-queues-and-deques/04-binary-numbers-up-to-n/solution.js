// O(n log n) time, O(n log n) space
function binaryNumbersUpTo(n) {
  const out = [];
  const queue = ["1"];
  let head = 0;
  for (let i = 0; i < n; i++) {
    const front = queue[head++];
    out.push(front);
    queue.push(front + "0");
    queue.push(front + "1");
  }
  return out;
}

console.log(binaryNumbersUpTo(5));
