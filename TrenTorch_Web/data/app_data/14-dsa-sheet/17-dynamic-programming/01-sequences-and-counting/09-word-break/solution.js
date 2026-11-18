// O(n * L) time, O(total characters in words) space
function wordBreak(s, words) {
  const trie = {};
  for (const word of words) {
    let node = trie;
    for (const ch of word) {
      if (!node[ch]) node[ch] = {};
      node = node[ch];
    }
    node['_'] = true; // mark end of word
  }

  const n = s.length;
  const reachable = new Array(n + 1).fill(false);
  reachable[0] = true;

  for (let i = 0; i < n; i++) {
    if (!reachable[i]) continue;
    let node = trie;
    for (let j = i; j < n; j++) {
      const ch = s[j];
      node = node[ch];
      if (!node) break;
      if (node['_']) reachable[j + 1] = true;
    }
  }

  return reachable[n];
}

console.log(wordBreak("leetcode", ["leet", "code"]));
