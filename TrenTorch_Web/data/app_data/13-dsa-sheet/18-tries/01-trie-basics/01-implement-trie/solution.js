// O(N) time, O(N) space where N is total length of all words
function runTrie(ops) {
  const root = {};

  function walk(word) {
    let node = root;
    for (const ch of word) {
      node = node[ch];
      if (node === undefined) return null;
    }
    return node;
  }

  const out = [];
  for (const op of ops) {
    const [kind, word] = op.split(' ');
    if (kind === 'insert') {
      let node = root;
      for (const ch of word) {
        if (node[ch] === undefined) node[ch] = {};
        node = node[ch];
      }
      node['$'] = true;
    } else if (kind === 'search') {
      const node = walk(word);
      out.push(node !== null && '$' in node);
    } else { // starts
      out.push(walk(word) !== null);
    }
  }
  return out;
}

console.log(runTrie(["insert apple", "search apple", "search app", "starts app", "insert app", "search app"]));
