// O(n) time, O(1) space
function secondLargest(nums) {
    let largest = null;
    let second = null;
    for (const x of nums) {
        if (largest === null || x > largest) {
            second = largest;
            largest = x;
        } else if (x < largest && (second === null || x > second)) {
            second = x;
        }
    }
    return second === null ? -1 : second;
}

console.log(secondLargest([4, 9, 9, 6]));
