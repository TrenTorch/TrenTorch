// O(log n) time, O(1) space
function countSquareLoop(n) {
  const N = typeof n === 'bigint' ? n : BigInt(n);
  let left = 0n;
  let right = N;
  let ans = 0n;
  while (left <= right) {
    const mid = (left + right) >> 1n;
    const midSq = mid * mid;
    if (midSq === N) {
      ans = mid;
      break;
    } else if (midSq < N) {
      ans = mid;
      left = mid + 1n;
    } else {
      right = mid - 1n;
    }
  }
  return Number(ans);
}

console.log(countSquareLoop(10));
