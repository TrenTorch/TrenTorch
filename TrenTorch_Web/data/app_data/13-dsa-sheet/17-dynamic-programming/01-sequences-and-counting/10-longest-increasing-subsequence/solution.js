// O(n log n) time, O(n) space
function lengthOfLis(nums) {
  const tails = [];
  for (let x of nums) {
    let lo = 0;
    let hi = tails.length;
    while (lo < hi) {
      const mid = (lo + hi) >> 1;
      if (tails[mid] < x) {
        lo = mid + 1;
      } else {
        hi = mid;
      }
    }
    if (lo === tails.length) {
      tails.push(x);
    } else {
      tails[lo] = x;
    }
  }
  return tails.length;
}

console.log(lengthOfLis([10, 9, 2, 5, 3, 7, 101, 18]));
