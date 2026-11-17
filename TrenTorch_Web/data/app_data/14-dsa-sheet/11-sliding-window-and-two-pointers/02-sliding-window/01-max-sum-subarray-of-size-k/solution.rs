// O(n) time, O(1) space
fn max_sum_k(nums: Vec<i64>, k: i64) -> i64 {
    let k = k as usize;
    let mut total: i64 = nums.iter().take(k).sum();
    let mut best = total;
    for i in k..nums.len() {
        total += nums[i] - nums[i - k];
        if total > best {
            best = total;
        }
    }
    best
}

fn main() {
    println!("{:?}", max_sum_k(vec![2, 1, 5, 1, 3, 2], 3));
}
