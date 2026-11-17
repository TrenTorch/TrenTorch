// O(L) time and O(L) space where L is length of term n
function countAndSay(n) {
  let term = "1";
  for (let i = 1; i < n; i++) {
    let next = "";
    let count = 1;
    for (let j = 0; j < term.length; j++) {
      if (j + 1 < term.length && term[j] === term[j + 1]) {
        count++;
      } else {
        next += count + term[j];
        count = 1;
      }
    }
    term = next;
  }
  return term;
}

console.log(countAndSay(4));
