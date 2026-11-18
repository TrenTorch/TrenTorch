// O(n^2) time, O(n) space for the sorted copy
fn three_sum_closest(nums: Vec<i64>, target: i64) -> i64 {
    let mut a = nums;
    a.sort();
    let n = a.len();
    let mut best = a[0] + a[1] + a[2];
    for i in 0..n.saturating_sub(2) {
        let mut lo = i + 1;
        let mut hi = n - 1;
        while lo < hi {
            let s = a[i] + a[lo] + a[hi];
            let diff = (s - target).abs();
            let best_diff = (best - target).abs();
            if diff < best_diff || (diff == best_diff && s < best) {
                best = s;
            }
            if s < target {
                lo += 1;
            } else if s > target {
                hi -= 1;
            } else {
                return s;
            }
        }
    }
    best
}

fn main() {
    println!("{:?}", three_sum_closest(vec![-1, 2, 1, -4], 1));
}
