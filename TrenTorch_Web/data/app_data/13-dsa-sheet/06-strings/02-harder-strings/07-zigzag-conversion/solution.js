// O(n) time, O(n) space
function zigzagConversion(s, rows) {
  if (rows === 1 || rows >= s.length) {
    return s;
  }
  const lines = Array.from({ length: rows }, () => []);
  let row = 0;
  let step = 1;
  for (let i = 0; i < s.length; i++) {
    lines[row].push(s[i]);
    if (row === 0) {
      step = 1;
    } else if (row === rows - 1) {
      step = -1;
    }
    row += step;
  }
  return lines.map(line => line.join('')).join('');
}

console.log(zigzagConversion("PAYPALISHIRING", 3));
