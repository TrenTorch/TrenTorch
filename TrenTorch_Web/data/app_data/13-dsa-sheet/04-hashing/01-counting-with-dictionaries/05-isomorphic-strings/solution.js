// O(n) time, O(n) space
function isomorphicStrings(s, t) {
  if (s.length !== t.length) return false;
  const forward = new Map();
  const backward = new Map();
  for (let i = 0; i < s.length; i++) {
    const a = s[i];
    const b = t[i];
    if (!forward.has(a)) forward.set(a, b);
    if (!backward.has(b)) backward.set(b, a);
    if (forward.get(a) !== b || backward.get(b) !== a) {
      return false;
    }
  }
  return true;
}

console.log(isomorphicStrings("egg", "add"));
