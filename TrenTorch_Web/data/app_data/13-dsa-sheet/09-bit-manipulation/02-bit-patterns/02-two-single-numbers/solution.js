// O(n) time, O(1) space
function twoSingleNumbers(nums) {
    let xorAll = 0;
    for (const x of nums) {
        xorAll ^= x;
    }
    const low = xorAll & -xorAll;
    let a = 0, b = 0;
    for (const x of nums) {
        if (x & low) {
            a ^= x;
        } else {
            b ^= x;
        }
    }
    return [Math.min(a, b), Math.max(a, b)];
}

console.log(twoSingleNumbers([1, 2, 1, 3, 2, 5]));
