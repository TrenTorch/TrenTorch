function minAddToMakeValid(s) {
  // O(n) time, O(1) space
  let openCount = 0;
  let need = 0;
  for (let ch of s) {
    if (ch === '(') {
      openCount++;
    } else if (openCount > 0) {
      openCount--;
    } else {
      need++;
    }
  }
  return need + openCount;
}

console.log(minAddToMakeValid("())"));
