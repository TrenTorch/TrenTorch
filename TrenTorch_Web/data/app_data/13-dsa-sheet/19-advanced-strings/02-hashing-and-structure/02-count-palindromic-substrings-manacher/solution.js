// O(n) time, O(n) space
function countPalindromesFast(s) {
  const n = s.length;
  let total = 0;
  const d1 = new Array(n).fill(0);
  let left = 0, right = -1;
  for (let i = 0; i < n; i++) {
    let k = i > right ? 1 : Math.min(d1[left + right - i], right - i + 1);
    while (i - k >= 0 && i + k < n && s[i - k] === s[i + k]) {
      k++;
    }
    d1[i] = k;
    total += k;
    if (i + k - 1 > right) {
      left = i - k + 1;
      right = i + k - 1;
    }
  }
  const d2 = new Array(n).fill(0);
  left = 0;
  right = -1;
  for (let i = 0; i < n; i++) {
    let k = i > right ? 0 : Math.min(d2[left + right - i + 1], right - i + 1);
    while (i - k - 1 >= 0 && i + k < n && s[i - k - 1] === s[i + k]) {
      k++;
    }
    d2[i] = k;
    total += k;
    if (i + k - 1 > right) {
      left = i - k;
      right = i + k - 1;
    }
  }
  return total;
}

console.log(countPalindromesFast("aaa"));
