// O(n^3) time, O(1) extra space (excluding output)
fn four_sum(nums: Vec<i64>, target: i64) -> Vec<Vec<i64>> {
    let mut a = nums;
    a.sort_unstable();
    let n = a.len();
    let mut out: Vec<Vec<i64>> = Vec::new();
    if n < 4 {
        return out;
    }
    for i in 0..(n - 3) {
        if i > 0 && a[i] == a[i - 1] {
            continue;
        }
        for j in (i + 1)..(n - 2) {
            if j > i + 1 && a[j] == a[j - 1] {
                continue;
            }
            let mut lo = j + 1;
            let mut hi = n - 1;
            while lo < hi {
                let total = a[i] + a[j] + a[lo] + a[hi];
                if total < target {
                    lo += 1;
                } else if total > target {
                    hi -= 1;
                } else {
                    out.push(vec![a[i], a[j], a[lo], a[hi]]);
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
    }
    out
}

fn main() {
    println!("{:?}", four_sum(vec![1, 0, -1, 0, -2, 2], 0));
}
