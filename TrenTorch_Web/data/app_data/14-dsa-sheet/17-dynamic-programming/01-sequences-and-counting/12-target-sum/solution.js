// O(n * sum) time, O(sum) space where sum = sum(nums)
function findTargetSumWays(nums, target) {
    let ways = {0: 1};
    for (const x of nums) {
        const nxt = {};
        for (const s in ways) {
            const sum = Number(s);
            const count = ways[s];
            const plus = sum + x;
            const minus = sum - x;
            nxt[plus] = (nxt[plus] || 0) + count;
            nxt[minus] = (nxt[minus] || 0) + count;
        }
        ways = nxt;
    }
    return ways[target] || 0;
}

console.log(findTargetSumWays([1, 1, 1, 1, 1], 3));
