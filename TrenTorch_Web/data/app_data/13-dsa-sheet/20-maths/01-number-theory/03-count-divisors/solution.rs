// O(sqrt(n)) time, O(1) space
fn count_divisors(n: i64) -> i64 {
    let mut count = 0;
    let mut d = 1;
    while d * d <= n {
        if n % d == 0 {
            if d * d == n {
                count += 1;
            } else {
                count += 2;
            }
        }
        d += 1;
    }
    count
}

fn main() {
    println!("{:?}", count_divisors(36));
}
