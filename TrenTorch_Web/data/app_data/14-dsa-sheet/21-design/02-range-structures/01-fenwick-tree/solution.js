// O((n + q) log n) time, O(n) space
function runFenwick(nums, ops) {
  const n = nums.length;
  const tree = new Array(n + 1).fill(0);
  const values = [...nums];

  function add(i, delta) {
    i += 1;
    while (i <= n) {
      tree[i] += delta;
      i += i & -i;
    }
  }

  function prefix(i) {
    let total = 0;
    while (i > 0) {
      total += tree[i];
      i -= i & -i;
    }
    return total;
  }

  for (let i = 0; i < n; i++) {
    add(i, nums[i]);
  }

  const out = [];
  for (const op of ops) {
    const parts = op.split(' ');
    if (parts[0] === 'set') {
      const i = parseInt(parts[1], 10);
      const v = parseInt(parts[2], 10);
      add(i, v - values[i]);
      values[i] = v;
    } else {
      const left = parseInt(parts[1], 10);
      const right = parseInt(parts[2], 10);
      out.push(prefix(right + 1) - prefix(left));
    }
  }
  return out;
}

console.log(runFenwick([1, 2, 3, 4], ["sum 0 3", "set 1 10", "sum 0 2", "sum 1 1"]));
