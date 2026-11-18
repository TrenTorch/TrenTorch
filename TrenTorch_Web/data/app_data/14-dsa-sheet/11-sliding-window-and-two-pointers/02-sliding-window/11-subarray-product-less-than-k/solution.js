// O(n) time, O(1) space
function countProductLess(nums, k) {
    let product = 1;
    let left = 0;
    let total = 0;
    for (let right = 0; right < nums.length; right++) {
        product *= nums[right];
        while (left <= right && product >= k) {
            product = Math.floor(product / nums[left]);
            left++;
        }
        total += right - left + 1;
    }
    return total;
}

console.log(countProductLess([10, 5, 2, 6], 100));
