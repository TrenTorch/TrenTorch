// O(n) time, O(1) space where n = b.len()
fn super_pow(a: i64, b: Vec<i64>) -> i64 {
    const MOD: i64 = 1337;
    let mut result = 1;
    for &digit in &b {
        result = (mod_pow(result, 10, MOD) * mod_pow(a, digit, MOD)) % MOD;
    }
    result
}

fn mod_pow(mut base: i64, mut exp: i64, modu: i64) -> i64 {
    let mut res = 1;
    base %= modu;
    while exp > 0 {
        if exp & 1 == 1 {
            res = (res * base) % modu;
        }
        base = (base * base) % modu;
        exp >>= 1;
    }
    res
}

fn main() {
    println!("{:?}", super_pow(2, vec![1, 0]));
}
