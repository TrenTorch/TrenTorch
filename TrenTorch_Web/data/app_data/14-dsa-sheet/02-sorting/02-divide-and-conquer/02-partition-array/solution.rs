// O(n) time, O(n) space
fn partition_array(nums: &[i64]) -> (Vec<i64>, usize) {
    let mut a = nums.to_vec();
    let n = a.len();
    let pivot = a[n - 1];
    let mut i: isize = -1;
    for j in 0..n - 1 {
        if a[j] <= pivot {
            i += 1;
            a.swap(i as usize, j);
        }
    }
    let pivot_idx = (i + 1) as usize;
    a.swap(pivot_idx, n - 1);
    (a, pivot_idx)
}

fn main() {
}
