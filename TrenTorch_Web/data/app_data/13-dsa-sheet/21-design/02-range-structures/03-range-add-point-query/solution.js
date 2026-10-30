function runRangeAdd(n, ops) {
  // O((n + m) log n) time, O(n) space where m = ops.length
  const tree = new Array(n + 2).fill(0);

  function add(i, delta) {
    i += 1;
    while (i <= n + 1) {
      tree[i] += delta;
      i += i & -i;
    }
  }

  function prefix(i) {
    let total = 0;
    i += 1;
    while (i > 0) {
      total += tree[i];
      i -= i & -i;
    }
    return total;
  }

  const out = [];
  for (const op of ops) {
    const parts = op.split(' ');
    if (parts[0] === 'add') {
      const left = parseInt(parts[1], 10);
      const right = parseInt(parts[2], 10);
      const v = parseInt(parts[3], 10);
      add(left, v);
      add(right + 1, -v);
    } else { // 'get'
      const idx = parseInt(parts[1], 10);
      out.push(prefix(idx));
    }
  }
  return out;
}

console.log(runRangeAdd(5, ["add 1 3 10", "get 2", "add 0 4 -1", "get 0", "get 3"]));
