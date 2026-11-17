// O(F) time, O(F * n) space where F is the number of generated strings
function noAdjacentOnes(n) {
  const out = [];

  function go(prefix) {
    if (prefix.length === n) {
      out.push(prefix);
      return;
    }
    go(prefix + '0');
    if (!prefix.endsWith('1')) {
      go(prefix + '1');
    }
  }

  go('');
  return out;
}

console.log(noAdjacentOnes(3));
