// O(n) time, O(n) space
function wordPattern(pattern, words) {
  if (pattern.length !== words.length) return false;
  const letterToWord = new Map();
  const wordToLetter = new Map();
  for (let i = 0; i < pattern.length; i++) {
    const letter = pattern[i];
    const word = words[i];
    if (!letterToWord.has(letter)) {
      letterToWord.set(letter, word);
    } else if (letterToWord.get(letter) !== word) {
      return false;
    }
    if (!wordToLetter.has(word)) {
      wordToLetter.set(word, letter);
    } else if (wordToLetter.get(word) !== letter) {
      return false;
    }
  }
  return true;
}

console.log(wordPattern("abba", ["dog", "cat", "cat", "dog"]));
