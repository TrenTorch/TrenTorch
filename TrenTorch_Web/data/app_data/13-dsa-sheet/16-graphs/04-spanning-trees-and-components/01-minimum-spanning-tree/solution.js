// O(m log m) time, O(n) space
function mstWeight(n, edges) {
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

  edges.sort((e1, e2) => e1[2] - e2[2]);

  let total = 0;
  let taken = 0;

  for (const [a, b, w] of edges) {
    let ra = find(a);
    let rb = find(b);
    if (ra !== rb) {
      if (size[ra] < size[rb]) {
        const tmp = ra;
        ra = rb;
        rb = tmp;
      }
      parent[rb] = ra;
      size[ra] += size[rb];
      total += w;
      taken += 1;
      if (taken === n - 1) break;
    }
  }

  return taken === n - 1 ? total : -1;
}

console.log(mstWeight(4, [[0, 1, 1], [1, 2, 2], [2, 3, 3], [0, 3, 10], [0, 2, 5]]));
