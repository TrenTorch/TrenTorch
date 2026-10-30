// O(sqrt(n)) time, O(1) space
function numSquares(n) {
  if (n === 0) return 0;
  const isPerfect = (x) => {
    const r = Math.floor(Math.sqrt(x));
    return r * r === x;
  };
  if (isPerfect(n)) return 1;

  let m = n;
  while (m % 4 === 0) {
    m = Math.floor(m / 4);
  }
  if (m % 8 === 7) return 4;

  for (let i = 1; i * i <= n; i++) {
    const rest = n - i * i;
    if (isPerfect(rest)) return 2;
  }
  return 3;
}

console.log(numSquares(12));
