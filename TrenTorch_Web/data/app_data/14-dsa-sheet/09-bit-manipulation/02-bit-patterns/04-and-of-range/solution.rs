// O(1) time, O(1) space
fn and_of_range(left: i64, right: i64) -> i64 {
    let xor = left ^ right;
    let shift = 64 - xor.leading_zeros();
    (left >> shift) << shift
}

fn main() {
    println!("{:?}", and_of_range(5, 7));
}
