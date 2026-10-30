// O(n*m) time, O(min(n,m)) space
function lcsLength(a, b) {
  if (b.length > a.length) {
    const tmp = a;
    a = b;
    b = tmp;
  }
  let prev = new Array(b.length + 1).fill(0);
  for (let i = 1; i <= a.length; i++) {
    const cur = new Array(b.length + 1).fill(0);
    const aChar = a[i - 1];
    for (let j = 1; j <= b.length; j++) {
      if (aChar === b[j - 1]) {
        cur[j] = prev[j - 1] + 1;
      } else {
        cur[j] = prev[j] > cur[j - 1] ? prev[j] : cur[j - 1];
      }
    }
    prev = cur;
  }
  return prev[b.length];
}

console.log(lcsLength("abcde", "ace"));
