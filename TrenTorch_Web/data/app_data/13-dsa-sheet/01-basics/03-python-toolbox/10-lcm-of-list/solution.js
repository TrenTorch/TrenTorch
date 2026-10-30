// O(n * log M) time, O(1) extra space
function gcd(a, b) {
  while (b !== 0n) {
    const t = a % b;
    a = b;
    b = t;
  }
  return a;
}

function lcm(a, b) {
  return (a / gcd(a, b)) * b;
}

function lcmOfList(nums) {
  let result = 1n;
  for (const x of nums) {
    result = lcm(result, BigInt(x));
  }
  return result.toString();
}

console.log(lcmOfList([4, 6, 10]));
