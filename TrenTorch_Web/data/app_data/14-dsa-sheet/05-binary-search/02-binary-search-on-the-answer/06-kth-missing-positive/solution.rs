// O(log n) time, O(1) space
fn kth_missing_positive(nums: Vec<i64>, k: i64) -> i64 {
    let mut lo = 0;
    let mut hi = nums.len();
    while lo < hi {
        let mid = (lo + hi) / 2;
        let missing = nums[mid] - (mid as i64 + 1);
        if missing < k {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    lo as i64 + k
}

fn main() {
    println!("{:?}", kth_missing_positive(vec![2, 3, 4, 7, 11], 5));
}
