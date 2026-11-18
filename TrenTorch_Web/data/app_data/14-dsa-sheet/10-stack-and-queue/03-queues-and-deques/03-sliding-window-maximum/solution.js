// O(n) time, O(k) space
function slidingWindowMax(nums, k) {
    const window = [];
    let head = 0;
    const out = [];
    for (let i = 0; i < nums.length; i++) {
        const x = nums[i];
        while (head < window.length && nums[window[window.length - 1]] <= x) {
            window.pop();
        }
        window.push(i);
        if (window[head] <= i - k) {
            head++;
        }
        if (i >= k - 1) {
            out.push(nums[window[head]]);
        }
    }
    return out;
}

console.log(slidingWindowMax([1, 3, -1, -3, 5, 3, 6, 7], 3));
