// O(sqrt(n)) time, O(1) space
fn count_divisor_steps(n: i64) -> i64 {
    let mut total: i64 = 0;
    let mut i: i64 = 1;
    while i <= n {
        let q = n / i;
        let j = n / q;
        total += q * (j - i + 1);
        i = j + 1;
    }
    total
}

fn main() {
    println!("{:?}", count_divisor_steps(5));
}
