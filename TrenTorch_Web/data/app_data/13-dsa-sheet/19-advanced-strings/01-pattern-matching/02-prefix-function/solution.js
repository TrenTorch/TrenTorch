function prefixFunction(s) {
  // O(n) time, O(n) space
  const n = s.length;
  const pi = new Array(n).fill(0);
  let k = 0;
  for (let i = 1; i < n; i++) {
    while (k > 0 && s[i] !== s[k]) {
      k = pi[k - 1];
    }
    if (s[i] === s[k]) {
      k++;
    }
    pi[i] = k;
  }
  return pi;
}

console.log(prefixFunction("abcabca"));
