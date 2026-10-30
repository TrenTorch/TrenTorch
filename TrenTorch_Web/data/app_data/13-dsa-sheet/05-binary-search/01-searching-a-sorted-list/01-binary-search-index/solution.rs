// O(log n) time, O(1) space
fn binary_search_index(nums: Vec<i64>, target: i64) -> i64 {
    let mut lo: i64 = 0;
    let mut hi: i64 = nums.len() as i64 - 1;
    while lo <= hi {
        let mid = (lo + hi) / 2;
        let mid_val = nums[mid as usize];
        if mid_val == target {
            return mid;
        }
        if mid_val < target {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    -1
}

fn main() {
    println!("{:?}", binary_search_index(vec![-1, 0, 3, 5, 9, 12], 9));
}
