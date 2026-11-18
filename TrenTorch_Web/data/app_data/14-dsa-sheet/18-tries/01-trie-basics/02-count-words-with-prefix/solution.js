// O(N * L + Q * L) time, O(N * L) space
function countWithPrefix(words, queries) {
  const root = { "#": 0 };
  for (const word of words) {
    let node = root;
    for (const ch of word) {
      if (!node[ch]) {
        node[ch] = { "#": 0 };
      }
      node = node[ch];
      node["#"]++;
    }
  }
  const out = [];
  for (const q of queries) {
    let node = root;
    for (const ch of q) {
      node = node[ch];
      if (node === undefined) break;
    }
    out.push(node ? node["#"] : 0);
  }
  return out;
}

console.log(countWithPrefix(["apple", "app", "apt", "bat"], ["ap", "app", "b", "c"]));
