// O(log n) time, O(1) space
fn count_digit_one(n: i64) -> i64 {
    let mut total = 0;
    let mut p = 1;
    while p <= n {
        let high = n / (p * 10);
        let cur = (n / p) % 10;
        let low = n % p;
        total += high * p;
        if cur > 1 {
            total += p;
        } else if cur == 1 {
            total += low + 1;
        }
        p *= 10;
    }
    total
}

fn main() {
    println!("{:?}", count_digit_one(13));
}
