// O(n) time, O(1) space
function rob(nums) {
    let skip = 0, take = 0;
    for (const x of nums) {
        const newSkip = Math.max(skip, take);
        take = skip + x;
        skip = newSkip;
    }
    return Math.max(skip, take);
}

console.log(rob([1, 2, 3, 1]));
