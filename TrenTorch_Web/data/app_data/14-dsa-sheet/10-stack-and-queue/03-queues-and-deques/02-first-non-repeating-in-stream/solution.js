// O(n) time, O(n) space
function firstNonRepeatingStream(s) {
  const counts = {};
  const queue = [];
  let front = 0;
  const out = [];
  for (const ch of s) {
    counts[ch] = (counts[ch] || 0) + 1;
    if (counts[ch] === 1) {
      queue.push(ch);
    }
    while (front < queue.length && counts[queue[front]] > 1) {
      front++;
    }
    out.push(front < queue.length ? queue[front] : '#');
  }
  return out.join('');
}

console.log(firstNonRepeatingStream("aabc"));
