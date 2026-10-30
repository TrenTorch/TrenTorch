// O(n) time, O(n) space
fn rotate_left(nums: Vec<i64>, k: i64) -> Vec<i64> {
    if nums.is_empty() {
        return Vec::new();
    }
    let n = nums.len();
    let k = (k % n as i64) as usize;
    let mut result = Vec::with_capacity(n);
    result.extend_from_slice(&nums[k..]);
    result.extend_from_slice(&nums[..k]);
    result
}

fn main() {
    println!("{:?}", rotate_left(vec![1, 2, 3, 4, 5], 2));
}
