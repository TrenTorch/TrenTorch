// O(log(min(m,n))) time, O(1) space
fn median_two_sorted(a: Vec<i64>, b: Vec<i64>) -> f64 {
    let (a, b) = if a.len() > b.len() { (b, a) } else { (a, b) };
    let m = a.len();
    let n = b.len();
    let half = (m + n + 1) / 2;
    let mut lo = 0;
    let mut hi = m;
    while lo <= hi {
        let i = (lo + hi) / 2;
        let j = half - i;
        let a_left = if i > 0 { a[i - 1] } else { i64::MIN };
        let a_right = if i < m { a[i] } else { i64::MAX };
        let b_left = if j > 0 { b[j - 1] } else { i64::MIN };
        let b_right = if j < n { b[j] } else { i64::MAX };
        if a_left <= b_right && b_left <= a_right {
            if (m + n) % 2 == 1 {
                return (a_left.max(b_left)) as f64;
            } else {
                let left_max = a_left.max(b_left) as f64;
                let right_min = a_right.min(b_right) as f64;
                return (left_max + right_min) / 2.0;
            }
        } else if a_left > b_right {
            hi = i - 1;
        } else {
            lo = i + 1;
        }
    }
    0.0
}

fn main() {
    println!("{:?}", median_two_sorted(vec![1, 3], vec![2]));
}
