// O(Catalan(n)) time, O(n) recursion stack + output space
function generateParentheses(n) {
  const out = [];
  function go(prefix, opens, closes) {
    if (prefix.length === 2 * n) {
      out.push(prefix);
      return;
    }
    if (opens < n) {
      go(prefix + '(', opens + 1, closes);
    }
    if (closes < opens) {
      go(prefix + ')', opens, closes + 1);
    }
  }
  go('', 0, 0);
  return out;
}

console.log(generateParentheses(3));
