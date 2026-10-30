// O(m * L) time, O(N * L) space where m = number of operations, L = max word length
function runWordDictionary(ops) {
  const root = {};
  const out = [];

  for (const op of ops) {
    const [kind, text] = op.split(' ');
    if (kind === 'add') {
      let node = root;
      for (const ch of text) {
        if (!Object.prototype.hasOwnProperty.call(node, ch)) {
          node[ch] = {};
        }
        node = node[ch];
      }
      node['$'] = true;
    } else {
      function go(node, i) {
        if (i === text.length) {
          return Object.prototype.hasOwnProperty.call(node, '$');
        }
        const ch = text[i];
        if (ch === '.') {
          for (const key in node) {
            if (key === '$') continue;
            if (go(node[key], i + 1)) return true;
          }
          return false;
        }
        if (Object.prototype.hasOwnProperty.call(node, ch)) {
          return go(node[ch], i + 1);
        }
        return false;
      }
      out.push(go(root, 0));
    }
  }

  return out;
}

console.log(runWordDictionary(["add bad", "add dad", "add mad", "search pad", "search bad", "search .ad", "search b.."]));
