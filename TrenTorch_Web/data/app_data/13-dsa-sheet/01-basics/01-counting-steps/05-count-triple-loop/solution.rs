// O(1) time, O(1) space
fn count_triple_loop(n: i64) -> i64 {
    n * (n + 1) * (n + 2) / 6
}

fn main() {
    println!("{:?}", count_triple_loop(3));
}
