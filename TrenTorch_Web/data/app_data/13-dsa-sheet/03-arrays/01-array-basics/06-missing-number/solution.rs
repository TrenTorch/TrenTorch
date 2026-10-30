// O(n) time, O(1) space
fn missing_number(nums: Vec<i64>) -> i64 {
    let n = nums.len() as i64;
    let total = n * (n + 1) / 2;
    let sum: i64 = nums.iter().sum();
    total - sum
}

fn main() {
    println!("{:?}", missing_number(vec![3, 0, 1]));
}
