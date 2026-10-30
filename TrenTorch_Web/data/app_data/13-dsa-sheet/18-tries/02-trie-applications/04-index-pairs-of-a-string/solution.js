// O(n * L) time, O(T) space where n = text length, L = max word length, T = total characters in words
function indexPairs(text, words) {
  const trie = {};
  for (const word of words) {
    let node = trie;
    for (const ch of word) {
      if (!node[ch]) node[ch] = {};
      node = node[ch];
    }
    node['$'] = true;
  }

  const out = [];
  const n = text.length;
  for (let i = 0; i < n; i++) {
    let node = trie;
    for (let j = i; j < n; j++) {
      node = node[text[j]];
      if (!node) break;
      if (node['$']) out.push([i, j]);
    }
  }
  return out;
}

console.log(indexPairs("thestoryofleetcodeandme", ["story", "fleet", "leetcode"]));
