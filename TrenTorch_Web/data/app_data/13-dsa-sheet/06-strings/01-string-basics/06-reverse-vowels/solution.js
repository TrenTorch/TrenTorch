function reverseVowels(s) {
  // O(n) time, O(n) space
  const vowelSet = new Set(['a','e','i','o','u','A','E','I','O','U']);
  const vowels = [];
  for (let i = 0; i < s.length; i++) {
    const ch = s[i];
    if (vowelSet.has(ch)) vowels.push(ch);
  }
  let idx = vowels.length - 1;
  let result = '';
  for (let i = 0; i < s.length; i++) {
    const ch = s[i];
    if (vowelSet.has(ch)) {
      result += vowels[idx--];
    } else {
      result += ch;
    }
  }
  return result;
}

console.log(reverseVowels("hello"));
