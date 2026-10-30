// O(1) time, O(1) space
fn count_pairs(n: i64) -> i64 {
    n * (n - 1) / 2
}

fn main() {
    println!("{:?}", count_pairs(4));
}
