// O(n*m) time, O(n+m) space where n,m are number of base-1e9 digits
function multiplyStrings(a, b) {
  if (a === "0" || b === "0") return "0";
  
  const BASE = 1000000000;
  const BASE_DIGITS = 9;
  
  // Convert string to array of ints in base 1e9, little-endian
  function toChunks(s) {
    const chunks = [];
    for (let i = s.length; i > 0; i -= BASE_DIGITS) {
      const start = Math.max(0, i - BASE_DIGITS);
      chunks.push(parseInt(s.slice(start, i), 10));
    }
    return chunks;
  }
  
  const aChunks = toChunks(a);
  const bChunks = toChunks(b);
  
  const result = new Array(aChunks.length + bChunks.length).fill(0);
  
  for (let i = 0; i < aChunks.length; i++) {
    let carry = 0;
    for (let j = 0; j < bChunks.length; j++) {
      const idx = i + j;
      const product = aChunks[i] * bChunks[j] + result[idx] + carry;
      result[idx] = product % BASE;
      carry = Math.floor(product / BASE);
    }
    result[i + bChunks.length] = carry;
  }
  
  // Remove leading zeros (most significant chunks)
  while (result.length > 1 && result[result.length - 1] === 0) {
    result.pop();
  }
  
  // Build result string
  let resStr = result[result.length - 1].toString();
  for (let i = result.length - 2; i >= 0; i--) {
    resStr += result[i].toString().padStart(BASE_DIGITS, '0');
  }
  return resStr;
}

console.log(multiplyStrings("123", "456"));
