// O(n) time, O(1) extra space (excluding output array)
function sortColors(nums) {
  let count0 = 0, count1 = 0, count2 = 0;
  for (let i = 0; i < nums.length; i++) {
    const v = nums[i];
    if (v === 0) count0++;
    else if (v === 1) count1++;
    else count2++;
  }
  const result = new Array(nums.length);
  let idx = 0;
  for (let i = 0; i < count0; i++) result[idx++] = 0;
  for (let i = 0; i < count1; i++) result[idx++] = 1;
  for (let i = 0; i < count2; i++) result[idx++] = 2;
  return result;
}

console.log(sortColors([2, 0, 2, 1, 1, 0]));
