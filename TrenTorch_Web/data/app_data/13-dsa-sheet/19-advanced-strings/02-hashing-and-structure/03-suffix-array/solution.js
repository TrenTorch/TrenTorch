function suffixArray(s) {
  // O(n log n) time, O(n) space
  if (!s || s.length === 0) return [];
  const text = [];
  for (let i = 0; i < s.length; i++) {
    text.push(s.charCodeAt(i) + 1);
  }
  text.push(0);
  const n = text.length;
  const maxText = Math.max(...text);
  const size = Math.max(maxText + 1, n);
  const order = new Array(n);
  let cls = new Array(n).fill(0);
  const count = new Array(size).fill(0);
  for (const v of text) count[v]++;
  for (let i = 1; i < size; i++) count[i] += count[i - 1];
  for (let i = n - 1; i >= 0; i--) {
    count[text[i]]--;
    order[count[text[i]]] = i;
  }
  let classes = 1;
  for (let i = 1; i < n; i++) {
    if (text[order[i]] !== text[order[i - 1]]) classes++;
    cls[order[i]] = classes - 1;
  }
  let shift = 1;
  while (shift < n) {
    const bySecond = new Array(n);
    for (let i = 0; i < n; i++) {
      bySecond[i] = (order[i] - shift + n) % n;
    }
    const cnt = new Array(classes).fill(0);
    for (let i = 0; i < n; i++) cnt[cls[bySecond[i]]]++;
    for (let i = 1; i < classes; i++) cnt[i] += cnt[i - 1];
    for (let i = n - 1; i >= 0; i--) {
      const c = cls[bySecond[i]];
      cnt[c]--;
      order[cnt[c]] = bySecond[i];
    }
    const newCls = new Array(n).fill(0);
    classes = 1;
    for (let i = 1; i < n; i++) {
      const a = order[i];
      const b = order[i - 1];
      if (cls[a] !== cls[b] || cls[(a + shift) % n] !== cls[(b + shift) % n]) {
        classes++;
      }
      newCls[a] = classes - 1;
    }
    cls = newCls;
    shift <<= 1;
  }
  return order.slice(1);
}

console.log(suffixArray("banana"));
