// O((n + q) log n) time, O(n) space
function runSegmentTree(nums, ops) {
  const n = nums.length;
  const inf = Infinity;
  const tree = new Array(2 * n).fill(inf);

  for (let i = 0; i < n; i++) {
    tree[n + i] = nums[i];
  }
  for (let i = n - 1; i >= 1; i--) {
    tree[i] = Math.min(tree[2 * i], tree[2 * i + 1]);
  }

  const out = [];

  for (const op of ops) {
    const parts = op.split(' ');
    if (parts[0] === 'set') {
      let i = parseInt(parts[1], 10) + n;
      tree[i] = parseInt(parts[2], 10);
      i = Math.floor(i / 2);
      while (i >= 1) {
        tree[i] = Math.min(tree[2 * i], tree[2 * i + 1]);
        i = Math.floor(i / 2);
      }
    } else {
      let lo = parseInt(parts[1], 10) + n;
      let hi = parseInt(parts[2], 10) + n + 1;
      let best = inf;
      while (lo < hi) {
        if (lo & 1) {
          best = Math.min(best, tree[lo]);
          lo++;
        }
        if (hi & 1) {
          hi--;
          best = Math.min(best, tree[hi]);
        }
        lo = Math.floor(lo / 2);
        hi = Math.floor(hi / 2);
      }
      out.push(best);
    }
  }

  return out;
}

console.log(runSegmentTree([5, 2, 8, 1], ["min 0 3", "set 3 9", "min 0 3", "min 2 3"]));
