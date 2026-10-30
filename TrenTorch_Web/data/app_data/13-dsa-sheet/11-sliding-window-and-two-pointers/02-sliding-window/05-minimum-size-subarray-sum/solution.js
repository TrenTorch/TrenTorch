// O(n) time, O(1) space
function minSubarrayLen(target, nums) {
    let best = nums.length + 1;
    let total = 0;
    let left = 0;
    for (let right = 0; right < nums.length; right++) {
        total += nums[right];
        while (total >= target) {
            best = Math.min(best, right - left + 1);
            total -= nums[left];
            left++;
        }
    }
    return best <= nums.length ? best : 0;
}

console.log(minSubarrayLen(7, [2, 3, 1, 2, 4, 3]));
