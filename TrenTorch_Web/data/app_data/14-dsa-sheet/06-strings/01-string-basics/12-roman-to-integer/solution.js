// O(n) time, O(1) space
function romanToInteger(s) {
  const values = { I: 1, V: 5, X: 10, L: 50, C: 100, D: 500, M: 1000 };
  let total = 0;
  for (let i = 0; i < s.length; i++) {
    const current = values[s[i]];
    const next = i + 1 < s.length ? values[s[i + 1]] : 0;
    if (next > current) {
      total -= current;
    } else {
      total += current;
    }
  }
  return total;
}

console.log(romanToInteger("III"));
