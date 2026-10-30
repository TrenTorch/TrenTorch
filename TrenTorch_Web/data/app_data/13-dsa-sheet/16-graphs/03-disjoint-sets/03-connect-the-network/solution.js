// O(n + m) time, O(n) space
function makeConnected(n, connections) {
  if (connections.length < n - 1) return -1;

  const parent = new Array(n);
  const size = new Array(n);
  for (let i = 0; i < n; i++) {
    parent[i] = i;
    size[i] = 1;
  }

  function find(a) {
    while (parent[a] !== a) {
      parent[a] = parent[parent[a]];
      a = parent[a];
    }
    return a;
  }

  let components = n;
  for (const [a, b] of connections) {
    let ra = find(a);
    let rb = find(b);
    if (ra !== rb) {
      if (size[ra] < size[rb]) {
        [ra, rb] = [rb, ra];
      }
      parent[rb] = ra;
      size[ra] += size[rb];
      components--;
    }
  }
  return components - 1;
}

console.log(makeConnected(4, [[0, 1], [0, 2], [1, 2]]));
