const MOD: i64 = 1_000_000_007;

// O(log n) time, O(log n) space
fn fib_mod(n: i64) -> i64 {
    fn pair(k: i64) -> (i64, i64) {
        if k == 0 {
            return (0, 1);
        }
        let (a, b) = pair(k / 2);
        let t = (2 * b - a).rem_euclid(MOD);
        let c = (a * t) % MOD;
        let e = (a * a + b * b) % MOD;
        if k % 2 == 0 {
            (c, e)
        } else {
            (e, (c + e) % MOD)
        }
    }
    pair(n).0
}

fn main() {
    println!("{:?}", fib_mod(10));
}
