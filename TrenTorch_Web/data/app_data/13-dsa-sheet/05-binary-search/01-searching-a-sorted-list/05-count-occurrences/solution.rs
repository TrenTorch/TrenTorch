// O(log n) time, O(1) space
fn count_occurrences(nums: Vec<i64>, target: i64) -> i64 {
    fn lower_bound(slice: &[i64], target: i64) -> usize {
        let mut lo = 0usize;
        let mut hi = slice.len();
        while lo < hi {
            let mid = (lo + hi) / 2;
            if slice[mid] < target {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        lo
    }

    fn upper_bound(slice: &[i64], target: i64) -> usize {
        let mut lo = 0usize;
        let mut hi = slice.len();
        while lo < hi {
            let mid = (lo + hi) / 2;
            if slice[mid] <= target {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        lo
    }

    let left = lower_bound(&nums, target);
    let right = upper_bound(&nums, target);
    (right - left) as i64
}

fn main() {
    println!("{:?}", count_occurrences(vec![1, 2, 2, 2, 3], 2));
}
