// O(n) time, O(1) space
fn max_product_subarray(nums: Vec<i64>) -> i64 {
    let mut best = nums[0];
    let mut hi = nums[0];
    let mut lo = nums[0];
    for &x in nums.iter().skip(1) {
        let a = x;
        let b = hi * x;
        let c = lo * x;
        hi = a.max(b.max(c));
        lo = a.min(b.min(c));
        if hi > best {
            best = hi;
        }
    }
    best
}

fn main() {
    println!("{:?}", max_product_subarray(vec![2, 3, -2, 4]));
}
