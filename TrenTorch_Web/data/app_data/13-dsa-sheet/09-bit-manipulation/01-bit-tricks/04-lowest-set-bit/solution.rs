fn lowest_set_bit(n: i64) -> i64 {
    // O(1) time, O(1) space
    n & -n
}

fn main() {
    println!("{:?}", lowest_set_bit(12));
}
