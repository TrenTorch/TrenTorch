// O(n) time, O(n) space
function pascalRow(row) {
  const out = [];
  let value = 1;
  for (let i = 0; i <= row; i++) {
    out.push(value);
    value = value * (row - i) / (i + 1);
  }
  return out;
}

console.log(pascalRow(4));
