// O(n) time, O(n) space
function reverseWords(s) {
  // Trim leading/trailing spaces, split by one or more spaces, reverse, and join with a single space
  return s.trim().split(/\s+/).reverse().join(' ');
}

console.log(reverseWords("the sky is blue"));
