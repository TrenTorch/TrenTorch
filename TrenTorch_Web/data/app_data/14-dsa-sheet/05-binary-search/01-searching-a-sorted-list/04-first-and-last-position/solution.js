// O(log n) time, O(1) space
function firstAndLast(nums, target) {
    let lo = 0, hi = nums.length;
    while (lo < hi) {
        let mid = Math.floor((lo + hi) / 2);
        if (nums[mid] < target) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    if (lo === nums.length || nums[lo] !== target) {
        return [-1, -1];
    }
    let first = lo;
    hi = nums.length;
    while (lo < hi) {
        let mid = Math.floor((lo + hi) / 2);
        if (nums[mid] <= target) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return [first, lo - 1];
}

console.log(firstAndLast([5, 7, 7, 8, 8, 10], 8));
