// O(n) time, O(1) space
function pivotIndex(nums) {
    let total = 0;
    for (const x of nums) {
        total += x;
    }
    let left = 0;
    for (let i = 0; i < nums.length; i++) {
        const x = nums[i];
        if (left === total - left - x) {
            return i;
        }
        left += x;
    }
    return -1;
}

console.log(pivotIndex([1, 7, 3, 6, 5, 6]));
