// O(n^2) time (dominated by sorting O(n log n)), O(1) extra space (excluding output)
fn three_sum(nums: Vec<i64>) -> Vec<Vec<i64>> {
    let mut a = nums;
    a.sort_unstable();
    let n = a.len();
    let mut out: Vec<Vec<i64>> = Vec::new();

    if n < 3 {
        return out;
    }

    for i in 0..(n - 2) {
        if i > 0 && a[i] == a[i - 1] {
            continue;
        }
        let mut lo = i + 1;
        let mut hi = n - 1;
        while lo < hi {
            let total = a[i] + a[lo] + a[hi];
            if total < 0 {
                lo += 1;
            } else if total > 0 {
                hi -= 1;
            } else {
                out.push(vec![a[i], a[lo], a[hi]]);
                lo += 1;
                hi -= 1;
                while lo < hi && a[lo] == a[lo - 1] {
                    lo += 1;
                }
                while lo < hi && a[hi] == a[hi + 1] {
                    hi -= 1;
                }
            }
        }
    }

    out
}

fn main() {
    println!("{:?}", three_sum(vec![-1, 0, 1, 2, -1, -4]));
}
