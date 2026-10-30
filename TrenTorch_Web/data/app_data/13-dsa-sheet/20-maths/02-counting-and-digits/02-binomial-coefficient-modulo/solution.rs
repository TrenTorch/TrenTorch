// O(min(k, n - k)) time, O(1) space (multiplicative formula with modular inverse)
fn binomial_mod(n: i64, k: i64) -> i64 {
    const MOD: i64 = 1_000_000_007;
    if k < 0 || k > n {
        return 0;
    }
    let k = std::cmp::min(k, n - k);
    let mut num: i64 = 1;
    let mut den: i64 = 1;
    for i in 0..k {
        num = num * ((n - i) % MOD) % MOD;
        den = den * ((i + 1) % MOD) % MOD;
    }
    num * mod_pow(den, MOD - 2, MOD) % MOD
}

fn mod_pow(mut base: i64, mut exp: i64, modulus: i64) -> i64 {
    let mut result: i64 = 1 % modulus;
    base %= modulus;
    while exp > 0 {
        if exp & 1 == 1 {
            result = result * base % modulus;
        }
        base = base * base % modulus;
        exp >>= 1;
    }
    result
}

fn main() {
    println!("{:?}", binomial_mod(5, 2));
}
