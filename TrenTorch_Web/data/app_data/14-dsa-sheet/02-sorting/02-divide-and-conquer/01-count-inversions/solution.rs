// O(n log n) time, O(n) space
fn count_inversions(nums: Vec<i64>) -> i64 {
    fn sort_count(a: &[i64]) -> (Vec<i64>, i64) {
        if a.len() <= 1 {
            return (a.to_vec(), 0);
        }
        let mid = a.len() / 2;
        let (left, x) = sort_count(&a[..mid]);
        let (right, y) = sort_count(&a[mid..]);
        let mut merged = Vec::with_capacity(a.len());
        let mut i = 0;
        let mut j = 0;
        let mut cross = 0i64;
        while i < left.len() && j < right.len() {
            if left[i] <= right[j] {
                merged.push(left[i]);
                i += 1;
            } else {
                merged.push(right[j]);
                j += 1;
                cross += (left.len() - i) as i64;
            }
        }
        if i < left.len() {
            merged.extend_from_slice(&left[i..]);
        }
        if j < right.len() {
            merged.extend_from_slice(&right[j..]);
        }
        (merged, x + y + cross)
    }

    let (_sorted, inv) = sort_count(&nums);
    inv
}

fn main() {
    println!("{:?}", count_inversions(vec![3, 1, 2]));
}
