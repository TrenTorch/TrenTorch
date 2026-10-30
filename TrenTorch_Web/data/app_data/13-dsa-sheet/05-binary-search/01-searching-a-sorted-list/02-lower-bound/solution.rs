// O(log n) time, O(1) space
fn lower_bound(nums: Vec<i64>, target: i64) -> i64 {
    let mut lo: i64 = 0;
    let mut hi: i64 = nums.len() as i64;
    while lo < hi {
        let mid = (lo + hi) / 2;
        if nums[mid as usize] < target {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    lo
}

fn main() {
    println!("{:?}", lower_bound(vec![1, 2, 2, 2, 5], 2));
}
