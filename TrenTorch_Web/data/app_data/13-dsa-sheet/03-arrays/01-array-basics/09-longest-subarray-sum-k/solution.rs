// O(n) time, O(1) space
fn longest_subarray_sum_k(nums: Vec<i64>, k: i64) -> i64 {
    let mut best: i64 = 0;
    let mut left: usize = 0;
    let mut total: i64 = 0;
    for (right, &x) in nums.iter().enumerate() {
        total += x;
        while total > k && left <= right {
            total -= nums[left];
            left += 1;
        }
        if total == k {
            let len = (right - left + 1) as i64;
            if len > best {
                best = len;
            }
        }
    }
    best
}

fn main() {
    println!("{:?}", longest_subarray_sum_k(vec![1, 2, 3, 1, 1, 1, 1], 3));
}
