// O(n + m) time, O(1) space
function ransomNote(note, magazine) {
  const counts = new Array(26).fill(0);
  for (let i = 0; i < magazine.length; i++) {
    counts[magazine.charCodeAt(i) - 97]++;
  }
  for (let i = 0; i < note.length; i++) {
    const idx = note.charCodeAt(i) - 97;
    if (counts[idx] === 0) return false;
    counts[idx]--;
  }
  return true;
}

console.log(ransomNote("aab", "baa"));
