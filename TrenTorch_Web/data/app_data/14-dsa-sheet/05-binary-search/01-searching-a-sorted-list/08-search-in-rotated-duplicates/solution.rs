// O(n) time, O(1) space
fn search_rotated_duplicates(nums: Vec<i64>, target: i64) -> bool {
    if nums.is_empty() {
        return false;
    }
    let mut lo: i64 = 0;
    let mut hi: i64 = nums.len() as i64 - 1;
    while lo <= hi {
        let mid = (lo + hi) / 2;
        let mid_usize = mid as usize;
        if nums[mid_usize] == target {
            return true;
        }
        let lo_usize = lo as usize;
        let hi_usize = hi as usize;
        if nums[lo_usize] == nums[mid_usize] && nums[mid_usize] == nums[hi_usize] {
            lo += 1;
            hi -= 1;
        } else if nums[lo_usize] <= nums[mid_usize] {
            if nums[lo_usize] <= target && target < nums[mid_usize] {
                hi = mid - 1;
            } else {
                lo = mid + 1;
            }
        } else {
            if nums[mid_usize] < target && target <= nums[hi_usize] {
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
    }
    false
}

fn main() {
    println!("{:?}", search_rotated_duplicates(vec![2, 5, 6, 0, 0, 1, 2], 0));
}
