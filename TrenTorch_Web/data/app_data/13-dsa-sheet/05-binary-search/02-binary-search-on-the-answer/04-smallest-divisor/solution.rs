// O(n log M) time, O(1) extra space where M = max(nums)
fn smallest_divisor(nums: Vec<i64>, threshold: i64) -> i64 {
    let mut lo: i64 = 1;
    let mut hi: i64 = *nums.iter().max().unwrap();
    while lo < hi {
        let mid = (lo + hi) / 2;
        let mut total: i64 = 0;
        for &x in &nums {
            // ceiling division: (x + mid - 1) / mid
            total += (x + mid - 1) / mid;
            if total > threshold {
                break; // early exit to avoid overflow
            }
        }
        if total <= threshold {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    lo
}

fn main() {
    println!("{:?}", smallest_divisor(vec![1, 2, 5, 9], 6));
}
