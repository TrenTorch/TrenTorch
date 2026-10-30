// O(n) time, O(n) space
function arrayLeaders(nums) {
  const out = [];
  let best = -Infinity;
  for (let i = nums.length - 1; i >= 0; i--) {
    const x = nums[i];
    if (x > best) {
      out.push(x);
      best = x;
    }
  }
  out.reverse();
  return out;
}

console.log(arrayLeaders([16, 17, 4, 3, 5, 2]));
