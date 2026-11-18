// O(n^2) time, O(n) space
function kthPermutation(n, k) {
  const remaining = [];
  for (let i = 1; i <= n; i++) remaining.push(i);

  k = k - 1;

  const fact = new Array(n + 1);
  fact[0] = 1;
  for (let i = 1; i <= n; i++) fact[i] = fact[i - 1] * i;

  const out = [];
  for (let size = n - 1; size >= 0; size--) {
    const f = fact[size];
    const index = Math.floor(k / f);
    k = k % f;
    out.push(String(remaining.splice(index, 1)[0]));
  }
  return out.join('');
}

console.log(kthPermutation(3, 3));
