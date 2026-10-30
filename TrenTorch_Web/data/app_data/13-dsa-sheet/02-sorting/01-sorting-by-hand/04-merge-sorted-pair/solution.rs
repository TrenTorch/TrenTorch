// O(n) time, O(n) space
fn merge_sorted_pair(a: Vec<i64>, b: Vec<i64>) -> (Vec<i64>, usize) {
    let mut merged = Vec::with_capacity(a.len() + b.len());
    let mut i = 0usize;
    let mut j = 0usize;
    let mut comparisons = 0usize;
    while i < a.len() && j < b.len() {
        comparisons += 1;
        if a[i] <= b[j] {
            merged.push(a[i]);
            i += 1;
        } else {
            merged.push(b[j]);
            j += 1;
        }
    }
    if i < a.len() {
        merged.extend_from_slice(&a[i..]);
    }
    if j < b.len() {
        merged.extend_from_slice(&b[j..]);
    }
    (merged, comparisons)
}

fn main() {
}
