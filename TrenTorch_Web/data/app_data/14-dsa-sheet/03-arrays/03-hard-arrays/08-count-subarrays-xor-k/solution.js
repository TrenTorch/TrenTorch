// O(n) time, O(n) space
function countSubarraysXorK(nums, k) {
  const seen = new Map();
  seen.set(0, 1);
  let prefix = 0;
  let count = 0;
  for (const x of nums) {
    prefix ^= x;
    const need = prefix ^ k;
    const add = seen.get(need);
    if (add !== undefined) {
      count += add;
    }
    seen.set(prefix, (seen.get(prefix) ?? 0) + 1);
  }
  return count;
}

console.log(countSubarraysXorK([4, 2, 2, 6, 4], 6));
