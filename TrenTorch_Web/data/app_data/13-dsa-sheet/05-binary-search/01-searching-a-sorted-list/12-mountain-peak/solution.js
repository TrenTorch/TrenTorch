// O(log n) time, O(1) space
function mountainPeak(nums) {
    let lo = 0;
    let hi = nums.length - 1;
    while (lo < hi) {
        const mid = Math.floor((lo + hi) / 2);
        if (nums[mid] < nums[mid + 1]) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return lo;
}

console.log(mountainPeak([1, 3, 5, 4, 2]));
