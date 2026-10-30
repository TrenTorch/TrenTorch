// O(log n) time, O(1) space
fn count_square_loop(n: i64) -> i64 {
    if n <= 0 {
        return 0;
    }
    let mut low = 1;
    let mut high = n;
    while low <= high {
        let mid = low + (high - low) / 2;
        if mid <= n / mid {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    high
}

fn main() {
    println!("{:?}", count_square_loop(10));
}
