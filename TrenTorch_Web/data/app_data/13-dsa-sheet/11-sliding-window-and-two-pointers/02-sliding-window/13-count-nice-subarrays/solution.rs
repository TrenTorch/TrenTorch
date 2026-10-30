// O(n) time, O(1) space
fn number_of_subarrays(nums: Vec<i64>, k: i64) -> i64 {
    fn at_most(nums: &[i64], m: i64) -> i64 {
        if m < 0 {
            return 0;
        }
        let mut odd: i64 = 0;
        let mut left: usize = 0;
        let mut total: i64 = 0;
        for right in 0..nums.len() {
            odd += nums[right] % 2;
            while odd > m {
                odd -= nums[left] % 2;
                left += 1;
            }
            total += (right + 1 - left) as i64;
        }
        total
    }
    at_most(&nums, k) - at_most(&nums, k - 1)
}

fn main() {
    println!("{:?}", number_of_subarrays(vec![1, 1, 2, 1, 1], 3));
}
