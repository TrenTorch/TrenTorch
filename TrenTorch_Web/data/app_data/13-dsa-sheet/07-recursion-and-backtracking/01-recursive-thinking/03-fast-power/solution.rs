// O(log exp) time, O(1) space
fn power_mod(base: i64, exp: i64, mod_: i64) -> i64 {
    if mod_ == 1 {
        return 0;
    }
    let mut result: i64 = 1 % mod_;
    let mut base = base % mod_;
    let mut exp = exp;
    while exp > 0 {
        if exp & 1 == 1 {
            result = (result * base) % mod_;
        }
        base = (base * base) % mod_;
        exp >>= 1;
    }
    result
}

fn main() {
    println!("{:?}", power_mod(2, 10, 1000));
}
