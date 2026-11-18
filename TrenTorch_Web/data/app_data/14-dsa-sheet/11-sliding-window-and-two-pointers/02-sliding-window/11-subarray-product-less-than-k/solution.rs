// O(n) time, O(1) space
fn count_product_less(nums: Vec<i64>, k: i64) -> i64 {
    let mut product: i64 = 1;
    let mut left: usize = 0;
    let mut total: i64 = 0;
    for right in 0..nums.len() {
        product *= nums[right];
        while left <= right && product >= k {
            product /= nums[left];
            left += 1;
        }
        total += (right + 1 - left) as i64;
    }
    total
}

fn main() {
    println!("{:?}", count_product_less(vec![10, 5, 2, 6], 100));
}
