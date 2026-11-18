// O(n) time, O(n) space
function subarraysKDistinct(nums, k) {
    function atMost(m) {
        if (m < 0) return 0;
        const count = new Map();
        let left = 0;
        let total = 0;
        for (let right = 0; right < nums.length; right++) {
            const x = nums[right];
            count.set(x, (count.get(x) || 0) + 1);
            while (count.size > m) {
                const leftVal = nums[left];
                count.set(leftVal, count.get(leftVal) - 1);
                if (count.get(leftVal) === 0) {
                    count.delete(leftVal);
                }
                left++;
            }
            total += right - left + 1;
        }
        return total;
    }
    return atMost(k) - atMost(k - 1);
}

console.log(subarraysKDistinct([1, 2, 1, 2, 3], 2));
