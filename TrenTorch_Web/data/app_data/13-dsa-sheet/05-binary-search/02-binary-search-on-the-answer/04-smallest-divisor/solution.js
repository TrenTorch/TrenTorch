// O(n log M) time, O(1) space where M = max(nums)
function smallestDivisor(nums, threshold) {
  let lo = 1;
  let hi = Math.max(...nums);
  while (lo < hi) {
    const mid = Math.floor((lo + hi) / 2);
    let sum = 0;
    for (const x of nums) {
      sum += Math.ceil(x / mid);
    }
    if (sum <= threshold) {
      hi = mid;
    } else {
      lo = mid + 1;
    }
  }
  return lo;
}

console.log(smallestDivisor([1, 2, 5, 9], 6));
