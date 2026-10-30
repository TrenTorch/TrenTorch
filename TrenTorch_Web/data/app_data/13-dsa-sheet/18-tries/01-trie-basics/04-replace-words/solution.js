// O(total roots length + total sentence characters) time, O(total roots length) space
function replaceWords(roots, sentence) {
  const trie = {};
  for (const root of roots) {
    let node = trie;
    for (const ch of root) {
      if (!node[ch]) node[ch] = {};
      node = node[ch];
    }
    node['$'] = true;
  }

  if (!sentence) return '';
  const words = sentence.split(' ');
  const out = [];
  for (const word of words) {
    let node = trie;
    let replaced = false;
    for (let i = 0; i < word.length; i++) {
      const ch = word[i];
      node = node[ch];
      if (!node) {
        out.push(word);
        replaced = true;
        break;
      }
      if (node['$']) {
        out.push(word.slice(0, i + 1));
        replaced = true;
        break;
      }
    }
    if (!replaced) out.push(word);
  }
  return out.join(' ');
}

console.log(replaceWords(["cat", "bat", "rat"], "the cattle was rattled by the battery"));
