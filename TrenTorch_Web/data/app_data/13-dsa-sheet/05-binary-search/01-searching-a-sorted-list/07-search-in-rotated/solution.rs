// O(log n) time, O(1) space
fn search_rotated(nums: Vec<i64>, target: i64) -> i64 {
    let mut lo = 0i64;
    let mut hi = (nums.len() as i64) - 1;
    while lo <= hi {
        let mid = (lo + hi) / 2;
        let mid_val = nums[mid as usize];
        if mid_val == target {
            return mid;
        }
        let lo_val = nums[lo as usize];
        if lo_val <= mid_val {
            if lo_val <= target && target < mid_val {
                hi = mid - 1;
            } else {
                lo = mid + 1;
            }
        } else {
            let hi_val = nums[hi as usize];
            if mid_val < target && target <= hi_val {
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
    }
    -1
}

fn main() {
    println!("{:?}", search_rotated(vec![4, 5, 6, 7, 0, 1, 2], 0));
}
