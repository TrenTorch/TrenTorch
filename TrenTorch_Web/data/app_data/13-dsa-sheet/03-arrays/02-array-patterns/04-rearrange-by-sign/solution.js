function rearrangeBySign(nums) {
  // O(n) time, O(n) space
  const pos = [];
  const neg = [];
  for (const x of nums) {
    if (x >= 0) pos.push(x);
    else neg.push(x);
  }
  const out = [];
  const maxLen = Math.max(pos.length, neg.length);
  for (let i = 0; i < maxLen; i++) {
    if (i < pos.length) out.push(pos[i]);
    if (i < neg.length) out.push(neg[i]);
  }
  return out;
}

console.log(rearrangeBySign([3, 1, -2, -5, 2, -4]));
