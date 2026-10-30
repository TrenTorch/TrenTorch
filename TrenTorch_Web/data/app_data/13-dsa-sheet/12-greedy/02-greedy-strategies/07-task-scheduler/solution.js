// O(N) time, O(1) space
function leastInterval(tasks, n) {
  if (!tasks || tasks.length === 0) {
    return 0;
  }
  const counts = {};
  for (let i = 0; i < tasks.length; i++) {
    const ch = tasks[i];
    counts[ch] = (counts[ch] || 0) + 1;
  }
  let maxFreq = 0;
  for (const freq of Object.values(counts)) {
    if (freq > maxFreq) maxFreq = freq;
  }
  let ties = 0;
  for (const freq of Object.values(counts)) {
    if (freq === maxFreq) ties++;
  }
  const part1 = (maxFreq - 1) * (n + 1) + ties;
  return Math.max(tasks.length, part1);
}

console.log(leastInterval("AAABBB", 2));
