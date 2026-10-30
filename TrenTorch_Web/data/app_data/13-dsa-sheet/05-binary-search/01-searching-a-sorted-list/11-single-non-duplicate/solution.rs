// O(log n) time, O(1) space
fn single_non_duplicate(nums: Vec<i64>) -> i64 {
    let mut lo: usize = 0;
    let mut hi: usize = nums.len() - 1;
    while lo < hi {
        let mut mid = (lo + hi) / 2;
        if mid % 2 == 1 {
            mid -= 1;
        }
        if nums[mid] == nums[mid + 1] {
            lo = mid + 2;
        } else {
            hi = mid;
        }
    }
    nums[lo]
}

fn main() {
    println!("{:?}", single_non_duplicate(vec![1, 1, 2, 3, 3, 4, 4, 8, 8]));
}
