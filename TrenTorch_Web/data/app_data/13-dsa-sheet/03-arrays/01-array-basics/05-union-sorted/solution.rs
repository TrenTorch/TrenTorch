// O(n+m) time, O(n+m) space
fn union_sorted(a: Vec<i64>, b: Vec<i64>) -> Vec<i64> {
    let mut out = Vec::new();
    let mut i = 0usize;
    let mut j = 0usize;
    let n = a.len();
    let m = b.len();
    while i < n || j < m {
        let x;
        if j == m || (i < n && a[i] <= b[j]) {
            x = a[i];
            i += 1;
        } else {
            x = b[j];
            j += 1;
        }
        if out.last().map_or(true, |&last| last != x) {
            out.push(x);
        }
    }
    out
}

fn main() {
    println!("{:?}", union_sorted(vec![1, 2, 2, 4], vec![2, 3, 4, 5]));
}
