// O(n) time, O(n) space
function nextGreater(nums) {
  const out = new Array(nums.length).fill(-1);
  const stack = [];
  for (let i = 0; i < nums.length; i++) {
    const x = nums[i];
    while (stack.length && nums[stack[stack.length - 1]] < x) {
      const idx = stack.pop();
      out[idx] = x;
    }
    stack.push(i);
  }
  return out;
}

console.log(nextGreater([2, 1, 2, 4, 3]));
