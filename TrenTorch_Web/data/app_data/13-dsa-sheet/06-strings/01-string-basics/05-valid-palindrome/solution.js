// O(n) time, O(1) space
function validPalindrome(s) {
  let i = 0, j = s.length - 1;
  while (i < j) {
    const ci = s[i];
    const cj = s[j];
    if (!isAlnum(ci)) {
      i++;
    } else if (!isAlnum(cj)) {
      j--;
    } else {
      if (ci.toLowerCase() !== cj.toLowerCase()) {
        return false;
      }
      i++;
      j--;
    }
  }
  return true;
}

function isAlnum(ch) {
  const code = ch.charCodeAt(0);
  return (
    (code >= 48 && code <= 57) || // 0-9
    (code >= 65 && code <= 90) || // A-Z
    (code >= 97 && code <= 122)   // a-z
  );
}

console.log(validPalindrome("A man, a plan, a canal: Panama"));
