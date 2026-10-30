// O(n) time, O(n) space
function nextGreaterCircular(nums) {
  const n = nums.length;
  const out = new Array(n).fill(-1);
  const stack = [];
  for (let i = 0; i < 2 * n; i++) {
    const x = nums[i % n];
    while (stack.length && nums[stack[stack.length - 1]] < x) {
      out[stack.pop()] = x;
    }
    if (i < n) {
      stack.push(i);
    }
  }
  return out;
}

console.log(nextGreaterCircular([1, 2, 1]));
