// O(n! * n) time, O(n) space (excluding output)
function distinctPermutations(s) {
  const counts = {};
  for (const ch of s) {
    counts[ch] = (counts[ch] || 0) + 1;
  }
  const letters = Object.entries(counts).sort((a, b) => a[0].localeCompare(b[0]));
  const left = letters.map(([, count]) => count);
  const n = s.length;
  const out = [];
  const prefix = [];

  function build() {
    if (prefix.length === n) {
      out.push(prefix.join(''));
      return;
    }
    for (let i = 0; i < letters.length; i++) {
      if (left[i] > 0) {
        left[i]--;
        prefix.push(letters[i][0]);
        build();
        prefix.pop();
        left[i]++;
      }
    }
  }

  build();
  return out;
}

console.log(distinctPermutations("abc"));
