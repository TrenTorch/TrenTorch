// O(n + m α(n)) time, O(n) space
function runUnionFind(n, ops) {
  const parent = new Array(n);
  const size = new Array(n).fill(1);
  for (let i = 0; i < n; i++) {
    parent[i] = i;
  }

  function find(x) {
    while (parent[x] !== x) {
      parent[x] = parent[parent[x]];
      x = parent[x];
    }
    return x;
  }

  const out = [];
  for (const op of ops) {
    const parts = op.split(' ');
    if (parts[0] === 'union') {
      let a = find(+parts[1]);
      let b = find(+parts[2]);
      if (a !== b) {
        if (size[a] < size[b]) {
          [a, b] = [b, a];
        }
        parent[b] = a;
        size[a] += size[b];
      }
    } else if (parts[0] === 'connected') {
      out.push(find(+parts[1]) === find(+parts[2]) ? 1 : 0);
    } else { // size
      out.push(size[find(+parts[1])]);
    }
  }
  return out;
}

console.log(runUnionFind(5, ["union 0 1", "union 1 2", "connected 0 2", "connected 0 3", "size 2"]));
