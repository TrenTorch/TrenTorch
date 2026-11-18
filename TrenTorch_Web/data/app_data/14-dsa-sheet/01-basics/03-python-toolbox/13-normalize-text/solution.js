// O(n) time, O(n) space
function normalizeText(s) {
  return s.toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
}

console.log(normalizeText("  Hello,   World!! 42 "));
