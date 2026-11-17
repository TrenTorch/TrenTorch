// O(n log M) time, O(1) space where M is max modulus
function gcd(a, b) {
    while (b !== 0) {
        const t = b;
        b = a % b;
        a = t;
    }
    return a;
}

function modInv(a, mod) {
    // returns inverse of a modulo mod, assuming gcd(a, mod) = 1
    let [old_r, r] = [a, mod];
    let [old_s, s] = [1, 0];
    while (r !== 0) {
        const q = Math.floor(old_r / r);
        [old_r, r] = [r, old_r - q * r];
        [old_s, s] = [s, old_s - q * s];
    }
    // old_r is gcd, old_s is inverse
    if (old_r !== 1) return null; // should not happen
    return ((old_s % mod) + mod) % mod;
}

function solveCongruences(remainders, moduli) {
    let x = 0;
    let modulus = 1;
    for (let i = 0; i < remainders.length; i++) {
        const r = remainders[i];
        const m = moduli[i];
        const g = gcd(modulus, m);
        if ((r - x) % g !== 0) {
            return -1;
        }
        const lcm = (modulus / g) * m;
        const a = modulus / g;
        const b = m / g;
        const inv = modInv(a, b);
        const diffDivG = (r - x) / g;
        const diffModB = ((diffDivG % b) + b) % b;
        const t = (diffModB * inv) % b;
        x = (x + modulus * t) % lcm;
        modulus = lcm;
    }
    return x;
}

console.log(solveCongruences([2, 3, 2], [3, 5, 7]));
