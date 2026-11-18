// O(|a| + |b|) time, O(|a|) space
function longestCommonSubstring(a, b) {
  const nxt = [{}];
  const link = [-1];
  const length = [0];
  let last = 0;

  for (const ch of a) {
    const cur = nxt.length;
    nxt.push({});
    length.push(length[last] + 1);
    link.push(0);
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
        length.push(length[p] + 1);
        link.push(link[q]);
        while (p !== -1 && nxt[p][ch] === q) {
          nxt[p][ch] = clone;
          p = link[p];
        }
        link[q] = link[cur] = clone;
      }
    }
    last = cur;
  }

  let best = 0, match = 0, state = 0;
  for (const ch of b) {
    while (state && !(ch in nxt[state])) {
      state = link[state];
      match = length[state];
    }
    if (ch in nxt[state]) {
      state = nxt[state][ch];
      match += 1;
    } else {
      state = match = 0;
    }
    if (match > best) best = match;
  }
  return best;
}

console.log(longestCommonSubstring("abcdxyz", "xyzabcd"));
