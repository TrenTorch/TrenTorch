// O(n) time, O(1) space
function maxWater(heights) {
  let left = 0;
  let right = heights.length - 1;
  let best = 0;
  while (left < right) {
    const area = Math.min(heights[left], heights[right]) * (right - left);
    if (area > best) best = area;
    if (heights[left] < heights[right]) {
      left++;
    } else {
      right--;
    }
  }
  return best;
}

console.log(maxWater([1, 8, 6, 2, 5, 4, 8, 3, 7]));
