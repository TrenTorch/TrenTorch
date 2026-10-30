// O(n) time, O(n) space
function addBinary(a, b) {
  const out = [];
  let i = a.length - 1;
  let j = b.length - 1;
  let carry = 0;
  while (i >= 0 || j >= 0 || carry) {
    let total = carry;
    if (i >= 0) {
      total += a.charCodeAt(i) - 48; // '0' -> 48
      i--;
    }
    if (j >= 0) {
      total += b.charCodeAt(j) - 48;
      j--;
    }
    out.push(String(total % 2));
    carry = Math.floor(total / 2);
  }
  return out.reverse().join('');
}

console.log(addBinary("11", "1"));
