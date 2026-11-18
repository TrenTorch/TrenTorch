// O(n) time, O(n) space
function repeatedDna(s) {
  const seen = new Set();
  const repeated = new Set();
  for (let i = 0; i <= s.length - 10; i++) {
    const part = s.slice(i, i + 10);
    if (seen.has(part)) {
      repeated.add(part);
    } else {
      seen.add(part);
    }
  }
  return Array.from(repeated).sort();
}

console.log(repeatedDna("AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"));
