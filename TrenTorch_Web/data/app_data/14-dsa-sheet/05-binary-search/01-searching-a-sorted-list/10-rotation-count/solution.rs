// O(log n) time, O(1) space
fn rotation_count(nums: Vec<i64>) -> i64 {
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
    lo as i64
}

fn main() {
    println!("{:?}", rotation_count(vec![3, 4, 5, 1, 2]));
}
