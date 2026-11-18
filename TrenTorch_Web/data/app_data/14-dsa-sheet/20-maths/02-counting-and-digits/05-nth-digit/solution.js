// O(log n) time, O(1) space
function nthDigit(n) {
    let length = 1;
    let count = 9;
    let start = 1;
    while (n > length * count) {
        n -= length * count;
        length++;
        count *= 10;
        start *= 10;
    }
    let number = start + Math.floor((n - 1) / length);
    return parseInt(number.toString()[(n - 1) % length], 10);
}

console.log(nthDigit(11));
