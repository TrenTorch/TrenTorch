// O(n) time, O(k) space
function subarraysDivisibleByK(nums, k) {
  const seen = new Map();
  seen.set(0, 1);
  let prefix = 0;
  let count = 0;
  
  for (const x of nums) {
    prefix = ((prefix + x) % k + k) % k;
    count += seen.get(prefix) || 0;
    seen.set(prefix, (seen.get(prefix) || 0) + 1);
  }
  
  return count;
}

console.log(subarraysDivisibleByK([4, 5, 0, -2, -3, 1], 5));
