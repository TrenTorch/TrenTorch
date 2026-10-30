// O(min(rows, cols) + log MOD) time, O(1) space
fn unique_paths(rows: i64, cols: i64) -> i64 {
    const MOD: i64 = 1_000_000_007;
    let n = rows + cols - 2;
    let k = std::cmp::min(rows - 1, cols - 1);
    let mut num: i64 = 1;
    let mut den: i64 = 1;
    for i in 1..=k {
        num = num * ((n - k + i) % MOD) % MOD;
        den = den * (i % MOD) % MOD;
    }
    num * mod_pow(den, MOD - 2, MOD) % MOD
}

fn mod_pow(mut base: i64, mut exp: i64, modulus: i64) -> i64 {
    let mut result: i64 = 1;
    base %= modulus;
    while exp > 0 {
        if (exp & 1) == 1 {
            result = result * base % modulus;
        }
        base = base * base % modulus;
        exp >>= 1;
    }
    result
}

fn main() {
    println!("{:?}", unique_paths(3, 7));
}
