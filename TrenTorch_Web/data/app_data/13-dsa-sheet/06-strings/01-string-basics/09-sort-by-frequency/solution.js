// O(n log n) time, O(n) space
function sortByFrequency(s) {
  const counts = new Map();
  for (const ch of s) {
    counts.set(ch, (counts.get(ch) || 0) + 1);
  }
  const chars = Array.from(counts.keys());
  chars.sort((a, b) => {
    const countA = counts.get(a);
    const countB = counts.get(b);
    if (countA !== countB) {
      return countB - countA;
    }
    return a.localeCompare(b);
  });
  let result = '';
  for (const ch of chars) {
    result += ch.repeat(counts.get(ch));
  }
  return result;
}

console.log(sortByFrequency("tree"));
