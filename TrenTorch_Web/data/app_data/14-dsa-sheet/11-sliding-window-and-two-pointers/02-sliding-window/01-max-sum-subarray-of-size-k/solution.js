// O(n) time, O(1) space
function maxSumK(nums, k) {
    let total = 0;
    for (let i = 0; i < k; i++) {
        total += nums[i];
    }
    let best = total;
    for (let i = k; i < nums.length; i++) {
        total += nums[i] - nums[i - k];
        if (total > best) best = total;
    }
    return best;
}

console.log(maxSumK([2, 1, 5, 1, 3, 2], 3));
