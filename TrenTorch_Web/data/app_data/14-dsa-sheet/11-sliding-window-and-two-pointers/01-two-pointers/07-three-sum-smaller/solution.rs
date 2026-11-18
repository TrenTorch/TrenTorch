// O(n^2) time, O(n) space for the sorted copy
fn count_triplets_smaller(nums: Vec<i64>, target: i64) -> i64 {
    let mut a = nums;
    a.sort();
    let n = a.len();
    let mut count: i64 = 0;
    for i in 0..n.saturating_sub(2) {
        let mut lo = i + 1;
        let mut hi = n - 1;
        while lo < hi {
            if a[i] + a[lo] + a[hi] < target {
                count += (hi - lo) as i64;
                lo += 1;
            } else {
                hi -= 1;
            }
        }
    }
    count
}

fn main() {
    println!("{:?}", count_triplets_smaller(vec![-2, 0, 1, 3], 2));
}
