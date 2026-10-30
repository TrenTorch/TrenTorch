// O(log_5 n) time, O(1) space
fn trailing_zeros(n: i64) -> i64 {
    let mut count = 0;
    let mut n = n;
    while n > 0 {
        n /= 5;
        count += n;
    }
    count
}

fn main() {
    println!("{:?}", trailing_zeros(25));
}
