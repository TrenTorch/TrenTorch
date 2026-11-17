// O(log n) time, O(1) space
fn floor_and_ceil(nums: Vec<i64>, target: i64) -> Vec<i64> {
    let mut lo = 0;
    let mut hi = nums.len();
    while lo < hi {
        let mid = (lo + hi) / 2;
        if nums[mid] < target {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    let ceil = if lo < nums.len() { nums[lo] } else { -1 };
    let floor = if lo < nums.len() && nums[lo] == target {
        target
    } else if lo > 0 {
        nums[lo - 1]
    } else {
        -1
    };
    vec![floor, ceil]
}

fn main() {
    println!("{:?}", floor_and_ceil(vec![1, 2, 8, 10, 11, 12, 19], 5));
}
