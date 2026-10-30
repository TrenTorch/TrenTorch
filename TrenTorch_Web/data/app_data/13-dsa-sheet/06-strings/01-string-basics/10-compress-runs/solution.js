// O(n) time, O(n) space
function compressRuns(s) {
  if (s.length === 0) return "";
  let result = "";
  let currentChar = s[0];
  let count = 1;
  
  for (let i = 1; i < s.length; i++) {
    if (s[i] === currentChar) {
      count++;
    } else {
      result += currentChar + (count > 1 ? count.toString() : "");
      currentChar = s[i];
      count = 1;
    }
  }
  result += currentChar + (count > 1 ? count.toString() : "");
  return result;
}

console.log(compressRuns("aabcccccaaa"));
