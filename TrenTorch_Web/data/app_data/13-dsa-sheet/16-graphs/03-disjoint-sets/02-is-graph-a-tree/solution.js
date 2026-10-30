// O(n α(n)) time, O(n) space
function validTree(n, edges) {
  if (n === 0 || edges.length !== n - 1) {
    return false;
  }
  const parent = Array.from({ length: n }, (_, i) => i);
  const size = new Array(n).fill(1);

  function find(a) {
    while (parent[a] !== a) {
      parent[a] = parent[parent[a]];
      a = parent[a];
    }
    return a;
  }

  for (const [a, b] of edges) {
    let ra = find(a);
    let rb = find(b);
    if (ra === rb) {
      return false;
    }
    if (size[ra] < size[rb]) {
      [ra, rb] = [rb, ra];
    }
    parent[rb] = ra;
    size[ra] += size[rb];
  }
  return true;
}

console.log(validTree(5, [[0, 1], [0, 2], [0, 3], [1, 4]]));
