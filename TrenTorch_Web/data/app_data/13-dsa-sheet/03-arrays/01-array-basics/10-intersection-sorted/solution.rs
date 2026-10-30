// O(n + m) time, O(k) space where k is the size of the output
fn intersection_sorted(a: Vec<i64>, b: Vec<i64>) -> Vec<i64> {
    let mut out = Vec::new();
    let mut i = 0usize;
    let mut j = 0usize;
    let len_a = a.len();
    let len_b = b.len();

    while i < len_a && j < len_b {
        if a[i] == b[j] {
            out.push(a[i]);
            i += 1;
            j += 1;
        } else if a[i] < b[j] {
            i += 1;
        } else {
            j += 1;
        }
    }

    out
}

fn main() {
    println!("{:?}", intersection_sorted(vec![1, 2, 2, 3], vec![2, 2, 2, 4]));
}
