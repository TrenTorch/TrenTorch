// O(1) time, O(1) space
fn count_doubling_steps(n: i64) -> i64 {
    let x = (n - 1) as u64;
    let bits = 64 - x.leading_zeros();
    bits as i64
}

fn main() {
    println!("{:?}", count_doubling_steps(8));
}
