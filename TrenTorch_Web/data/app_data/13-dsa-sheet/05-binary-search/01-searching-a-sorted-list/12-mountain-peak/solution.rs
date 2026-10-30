// O(log n) time, O(1) space
fn mountain_peak(nums: Vec<i64>) -> i64 {
    let mut lo: usize = 0;
    let mut hi: usize = nums.len() - 1;
    while lo < hi {
        let mid = (lo + hi) / 2;
        if nums[mid] < nums[mid + 1] {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    lo as i64
}

fn main() {
    println!("{:?}", mountain_peak(vec![1, 3, 5, 4, 2]));
}
