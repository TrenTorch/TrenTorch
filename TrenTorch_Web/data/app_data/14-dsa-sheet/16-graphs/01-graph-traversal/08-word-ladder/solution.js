// O(n * m^2) time, O(n * m) space where n = words.length, m = word length
function ladderLength(begin, end, words) {
  const allowed = new Set(words);
  if (!allowed.has(end)) return 0;

  const groups = new Map();
  const allWords = new Set(allowed);
  allWords.add(begin);

  for (const word of allWords) {
    for (let i = 0; i < word.length; i++) {
      const pattern = word.slice(0, i) + '*' + word.slice(i + 1);
      if (!groups.has(pattern)) {
        groups.set(pattern, []);
      }
      groups.get(pattern).push(word);
    }
  }

  const seen = new Set([begin]);
  const queue = [[begin, 1]];
  let head = 0;

  while (head < queue.length) {
    const [word, steps] = queue[head++];
    if (word === end) return steps;

    for (let i = 0; i < word.length; i++) {
      const pattern = word.slice(0, i) + '*' + word.slice(i + 1);
      const neighbors = groups.get(pattern) || [];
      for (const other of neighbors) {
        if (!seen.has(other)) {
          seen.add(other);
          queue.push([other, steps + 1]);
        }
      }
    }
  }

  return 0;
}

console.log(ladderLength("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]));
