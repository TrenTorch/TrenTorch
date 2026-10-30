// O(n) time, O(1) space
fn repeating_and_missing(nums: Vec<i64>) -> Vec<i64> {
    let n = nums.len() as i64;
    let mut sum = 0i64;
    let mut sum_sq = 0i64;
    for &x in &nums {
        sum += x;
        sum_sq += x * x;
    }
    let expected_sum = n * (n + 1) / 2;
    let expected_sq = n * (n + 1) * (2 * n + 1) / 6;
    let diff = sum - expected_sum; // repeated - missing
    let square_diff = sum_sq - expected_sq; // repeated^2 - missing^2
    let plus = square_diff / diff; // repeated + missing
    let repeated = (plus + diff) / 2;
    let missing = (plus - diff) / 2;
    vec![repeated, missing]
}

fn main() {
    println!("{:?}", repeating_and_missing(vec![3, 1, 2, 5, 3]));
}
