// O(n) time, O(1) space
function trapWater(heights) {
    let left = 0;
    let right = heights.length - 1;
    let leftMax = 0;
    let rightMax = 0;
    let total = 0;
    while (left < right) {
        if (heights[left] < heights[right]) {
            leftMax = Math.max(leftMax, heights[left]);
            total += leftMax - heights[left];
            left++;
        } else {
            rightMax = Math.max(rightMax, heights[right]);
            total += rightMax - heights[right];
            right--;
        }
    }
    return total;
}

console.log(trapWater([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]));
