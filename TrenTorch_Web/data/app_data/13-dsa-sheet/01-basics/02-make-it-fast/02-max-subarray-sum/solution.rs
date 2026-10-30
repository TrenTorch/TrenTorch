// O(n) time, O(1) space
fn max_subarray_sum(nums: Vec<i64>) -> i64 {
    let mut best = nums[0];
    let mut cur = nums[0];
    for &x in &nums[1..] {
        cur = x.max(cur + x);
        if cur > best {
            best = cur;
        }
    }
    best
}

fn main() {
    println!("{:?}", max_subarray_sum(vec![-2, 1, -3, 4, -1, 2, 1, -5, 4]));
}
