// O(n) time worst case (all duplicates), O(log n) average, O(1) space
function searchRotatedDuplicates(nums, target) {
    let lo = 0;
    let hi = nums.length - 1;
    while (lo <= hi) {
        const mid = Math.floor((lo + hi) / 2);
        if (nums[mid] === target) {
            return true;
        }
        if (nums[lo] === nums[mid] && nums[mid] === nums[hi]) {
            lo += 1;
            hi -= 1;
        } else if (nums[lo] <= nums[mid]) {
            if (nums[lo] <= target && target < nums[mid]) {
                hi = mid - 1;
            } else {
                lo = mid + 1;
            }
        } else {
            if (nums[mid] < target && target <= nums[hi]) {
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
    }
    return false;
}

console.log(searchRotatedDuplicates([2, 5, 6, 0, 0, 1, 2], 0));
