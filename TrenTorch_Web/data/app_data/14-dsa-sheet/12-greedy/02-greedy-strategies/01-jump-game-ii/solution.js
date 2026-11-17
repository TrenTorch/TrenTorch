// O(n) time, O(1) space
function minJumps(nums) {
  const n = nums.length;
  if (n <= 1) return 0;
  let jumps = 0;
  let end = 0;
  let far = 0;
  for (let i = 0; i < n - 1; i++) {
    far = Math.max(far, i + nums[i]);
    if (i === far) return -1;
    if (i === end) {
      jumps++;
      end = far;
      if (end >= n - 1) break;
    }
  }
  return end >= n - 1 ? jumps : -1;
}

console.log(minJumps([2, 3, 1, 1, 4]));
