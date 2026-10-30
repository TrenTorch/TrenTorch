// O(1) time, O(1) space
function minFlips(a, b, c) {
    let flips = 0;
    for (let i = 0; i < 31; i++) {
        const x = (a >> i) & 1;
        const y = (b >> i) & 1;
        const z = (c >> i) & 1;
        if (z === 0) {
            flips += x + y;
        } else if (x === 0 && y === 0) {
            flips += 1;
        }
    }
    return flips;
}

console.log(minFlips(2, 6, 5));
