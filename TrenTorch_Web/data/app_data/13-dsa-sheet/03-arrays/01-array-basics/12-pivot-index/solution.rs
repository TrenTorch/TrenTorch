// O(n) time, O(1) space
fn pivot_index(nums: Vec<i64>) -> i64 {
    let total: i64 = nums.iter().sum();
    let mut left = 0;
    for (i, &x) in nums.iter().enumerate() {
        if left == total - left - x {
            return i as i64;
        }
        left += x;
    }
    -1
}

fn main() {
    println!("{:?}", pivot_index(vec![1, 7, 3, 6, 5, 6]));
}
