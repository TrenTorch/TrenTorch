// O(n α(n)) time, O(n) space
function findRedundantConnection(edges) {
  const parent = new Array(edges.length + 2);
  const size = new Array(edges.length + 2).fill(1);
  for (let i = 0; i < parent.length; i++) parent[i] = i;

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
      return [a, b];
    }
    if (size[ra] < size[rb]) {
      [ra, rb] = [rb, ra];
    }
    parent[rb] = ra;
    size[ra] += size[rb];
  }
  return [];
}

console.log(findRedundantConnection([[1, 2], [1, 3], [2, 3]]));
