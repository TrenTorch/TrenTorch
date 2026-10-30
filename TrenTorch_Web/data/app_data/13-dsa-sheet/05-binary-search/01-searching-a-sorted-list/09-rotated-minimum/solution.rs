// O(log n) time, O(1) space
fn rotated_minimum(nums: Vec<i64>) -> i64 {
    let mut lo: usize = 0;
    let mut hi: usize = nums.len() - 1;
    while lo < hi {
        let mid = (lo + hi) / 2;
        if nums[mid] > nums[hi] {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    nums[lo]
}

fn main() {
    println!("{:?}", rotated_minimum(vec![4, 5, 6, 7, 0, 1, 2]));
}
