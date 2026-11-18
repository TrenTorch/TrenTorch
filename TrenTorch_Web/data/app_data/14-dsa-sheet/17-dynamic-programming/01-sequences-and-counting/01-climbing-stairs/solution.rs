const MOD: i64 = 1_000_000_007;

// O(log n) time, O(log n) space
fn fib(k: i64) -> (i64, i64) {
    if k == 0 {
        return (0, 1);
    }
    let (a, b) = fib(k >> 1);
    let two_b = (2 * b) % MOD;
    let diff = (two_b - a + MOD) % MOD;
    let c = (a * diff) % MOD;
    let d = (a * a + b * b) % MOD;
    if k & 1 == 1 {
        (d, (c + d) % MOD)
    } else {
        (c, d)
    }
}

fn climb_stairs(n: i64) -> i64 {
    fib(n + 1).0
}

fn main() {
    println!("{:?}", climb_stairs(3));
}
