fn count_halving_steps(n: i64) -> i64 {
    // O(1) time, O(1) space
    (64 - n.leading_zeros() - 1) as i64
}

fn main() {
    println!("{:?}", count_halving_steps(8));
}
