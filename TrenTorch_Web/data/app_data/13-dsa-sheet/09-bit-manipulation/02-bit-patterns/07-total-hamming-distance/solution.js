// O(n) time, O(1) space
function totalHammingDistance(nums) {
  const n = nums.length;
  let total = 0;
  for (let i = 0; i < 30; i++) {
    let ones = 0;
    for (const x of nums) {
      ones += (x >> i) & 1;
    }
    total += ones * (n - ones);
  }
  return total;
}

console.log(totalHammingDistance([4, 14, 2]));
