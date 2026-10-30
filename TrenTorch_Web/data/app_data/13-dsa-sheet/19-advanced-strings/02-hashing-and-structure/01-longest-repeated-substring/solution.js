// O(n) time, O(n) space
function longestRepeatedLength(s) {
  const nxt = [{}];
  const link = [-1];
  const length = [0];
  const occ = [0];
  let last = 0;

  for (const ch of s) {
    const cur = nxt.length;
    nxt.push({});
    link.push(0);
    length.push(length[last] + 1);
    occ.push(1);
    let p = last;
    while (p !== -1 && !(ch in nxt[p])) {
      nxt[p][ch] = cur;
      p = link[p];
    }
    if (p !== -1) {
      const q = nxt[p][ch];
      if (length[p] + 1 === length[q]) {
        link[cur] = q;
      } else {
        const clone = nxt.length;
        nxt.push({ ...nxt[q] });
        link.push(link[q]);
        length.push(length[p] + 1);
        occ.push(0);
        while (p !== -1 && nxt[p][ch] === q) {
          nxt[p][ch] = clone;
          p = link[p];
        }
        link[q] = link[cur] = clone;
      }
    }
    last = cur;
  }

  const byLength = Array.from({ length: s.length + 1 }, () => []);
  for (let v = 1; v < nxt.length; v++) {
    byLength[length[v]].push(v);
  }
  let best = 0;
  for (let size = s.length; size > 0; size--) {
    for (const v of byLength[size]) {
      if (occ[v] >= 2) {
        best = Math.max(best, size);
      }
      occ[link[v]] += occ[v];
    }
  }
  return best;
}

console.log(longestRepeatedLength("banana"));
