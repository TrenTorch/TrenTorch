// O(log n) time, O(1) space
function kthMissingPositive(nums, k) {
    let lo = 0;
    let hi = nums.length;
    while (lo < hi) {
        const mid = Math.floor((lo + hi) / 2);
        if (nums[mid] - (mid + 1) < k) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return lo + k;
}

console.log(kthMissingPositive([2, 3, 4, 7, 11], 5));
