function integerToRoman(num) {
  // O(1) time, O(1) space
  const table = [
    [1000, "M"],
    [900, "CM"],
    [500, "D"],
    [400, "CD"],
    [100, "C"],
    [90, "XC"],
    [50, "L"],
    [40, "XL"],
    [10, "X"],
    [9, "IX"],
    [5, "V"],
    [4, "IV"],
    [1, "I"]
  ];
  const out = [];
  for (const [value, symbol] of table) {
    const count = Math.floor(num / value);
    num %= value;
    out.push(symbol.repeat(count));
  }
  return out.join("");
}

console.log(integerToRoman(3));
