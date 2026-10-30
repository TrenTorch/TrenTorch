// O(log budget) time, O(1) space
function bitLength(x) {
  let len = 0n;
  let y = x;
  while (y > 0n) {
    y >>= 1n;
    len++;
  }
  return len;
}

function _cost(growth, n) {
  if (growth === "n") {
    return n;
  }
  if (growth === "n log n") {
    return n * (bitLength(n) - 1n);
  }
  if (growth === "n^2") {
    return n * n;
  }
  // growth === "n^3"
  return n * n * n;
}

function largestN(growth, budget) {
  const B = BigInt(budget);
  if (growth === "2^n") {
    if (B < 2n) return "0";
    return (bitLength(B) - 1n).toString();
  }
  if (_cost(growth, 1n) > B) return "0";
  let lo = 1n;
  let hi = B + 1n;
  while (lo < hi) {
    const mid = (lo + hi + 1n) / 2n;
    if (_cost(growth, mid) <= B) {
      lo = mid;
    } else {
      hi = mid - 1n;
    }
  }
  return lo.toString();
}

console.log(largestN("n^2", 100));
