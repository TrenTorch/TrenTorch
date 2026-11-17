// O(N * L) time, O(1) extra space
function longestCommonPrefix(words) {
  if (!words || words.length === 0) return "";
  let minWord = words[0];
  let maxWord = words[0];
  for (let i = 1; i < words.length; i++) {
    const w = words[i];
    if (w < minWord) minWord = w;
    if (w > maxWord) maxWord = w;
  }
  let i = 0;
  const limit = Math.min(minWord.length, maxWord.length);
  while (i < limit && minWord[i] === maxWord[i]) {
    i++;
  }
  return minWord.slice(0, i);
}

console.log(longestCommonPrefix(["flower", "flow", "flight"]));
