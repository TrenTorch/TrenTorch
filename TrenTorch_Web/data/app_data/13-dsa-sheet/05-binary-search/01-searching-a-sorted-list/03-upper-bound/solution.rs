// O(log n) time, O(1) space
fn upper_bound(nums: Vec<i64>, target: i64) -> i64 {
    let mut lo: usize = 0;
    let mut hi: usize = nums.len();
    while lo < hi {
        let mid = (lo + hi) / 2;
        if nums[mid] <= target {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    lo as i64
}

fn main() {
    println!("{:?}", upper_bound(vec![1, 2, 2, 2, 5], 2));
}
