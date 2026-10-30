// O(n) time, O(1) space where n = b.length
function powmod(base, exp, mod) {
    let result = 1;
    base = base % mod;
    while (exp > 0) {
        if (exp % 2 === 1) result = (result * base) % mod;
        base = (base * base) % mod;
        exp = Math.floor(exp / 2);
    }
    return result;
}

function superPow(a, b) {
    const mod = 1337;
    let result = 1;
    for (let digit of b) {
        result = (powmod(result, 10, mod) * powmod(a, digit, mod)) % mod;
    }
    return result;
}

console.log(superPow(2, [1, 0]));
