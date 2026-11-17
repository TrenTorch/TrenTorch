// O(N * L) time, O(N * L) space where N is number of words and L is max word length
function minimumLengthEncoding(words) {
  const trie = Object.create(null);
  const ends = [];
  const unique = new Set(words);
  for (const word of unique) {
    let node = trie;
    for (let i = word.length - 1; i >= 0; i--) {
      const ch = word[i];
      if (!node[ch]) node[ch] = Object.create(null);
      node = node[ch];
    }
    ends.push([node, word.length]);
  }
  let total = 0;
  for (const [node, length] of ends) {
    if (Object.keys(node).length === 0) total += length + 1;
  }
  return total;
}

console.log(minimumLengthEncoding(["time", "me", "bell"]));
