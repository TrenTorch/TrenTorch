// O(n) time, O(n) space
fn move_zeros(nums: Vec<i64>) -> Vec<i64> {
    let non_zero: Vec<i64> = nums.iter().filter(|&&x| x != 0).cloned().collect();
    let zero_count = nums.len() - non_zero.len();
    let mut result = non_zero;
    result.extend(std::iter::repeat(0).take(zero_count));
    result
}

fn main() {
    println!("{:?}", move_zeros(vec![0, 1, 0, 3, 12]));
}
