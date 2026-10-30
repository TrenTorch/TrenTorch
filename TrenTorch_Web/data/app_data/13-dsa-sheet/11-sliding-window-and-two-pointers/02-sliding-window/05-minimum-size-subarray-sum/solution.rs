// O(n) time, O(1) space
fn min_subarray_len(target: i64, nums: Vec<i64>) -> i64 {
    let n = nums.len();
    let mut best: usize = n + 1;
    let mut total: i64 = 0;
    let mut left: usize = 0;
    for right in 0..n {
        total += nums[right];
        while total >= target {
            best = best.min(right - left + 1);
            total -= nums[left];
            left += 1;
        }
    }
    if best <= n {
        best as i64
    } else {
        0
    }
}

fn main() {
    println!("{:?}", min_subarray_len(7, vec![2, 3, 1, 2, 4, 3]));
}
