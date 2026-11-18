// O(sqrt(n)) time, O(1) space (divisor-pair counting)
fn sum_divisor_counts(n: i64) -> i64 {
    let r = isqrt_i64(n);
    let mut s: i64 = 0;
    for j in 1..=r {
        s += n / j;
    }
    2 * s - r * r
}

fn isqrt_i64(n: i64) -> i64 {
    if n < 2 {
        return n.max(0);
    }
    let mut x = (n as f64).sqrt() as i64;
    while x * x > n {
        x -= 1;
    }
    while (x + 1) * (x + 1) <= n {
        x += 1;
    }
    x
}

fn main() {
    println!("{:?}", sum_divisor_counts(5));
}
