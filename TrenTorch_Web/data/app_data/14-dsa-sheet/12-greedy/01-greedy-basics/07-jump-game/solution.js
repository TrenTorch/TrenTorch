// O(n) time, O(1) space
function canJump(nums) {
    let far = 0;
    for (let i = 0; i < nums.length; i++) {
        if (i > far) return false;
        far = Math.max(far, i + nums[i]);
    }
    return true;
}

console.log(canJump([2, 3, 1, 1, 4]));
