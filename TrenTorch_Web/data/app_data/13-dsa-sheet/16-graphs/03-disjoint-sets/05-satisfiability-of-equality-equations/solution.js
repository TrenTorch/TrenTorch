// O(n) time, O(1) space
function equationsPossible(equations) {
  const parent = Array.from({ length: 26 }, (_, i) => i);

  function find(a) {
    while (parent[a] !== a) {
      parent[a] = parent[parent[a]];
      a = parent[a];
    }
    return a;
  }

  // Union all equalities
  for (const eq of equations) {
    if (eq[1] === '=') {
      const x = eq.charCodeAt(0) - 97;
      const y = eq.charCodeAt(3) - 97;
      parent[find(x)] = find(y);
    }
  }

  // Check all inequalities
  for (const eq of equations) {
    if (eq[1] === '!') {
      const x = eq.charCodeAt(0) - 97;
      const y = eq.charCodeAt(3) - 97;
      if (find(x) === find(y)) {
        return false;
      }
    }
  }

  return true;
}

console.log(equationsPossible(["a==b", "b!=a"]));
