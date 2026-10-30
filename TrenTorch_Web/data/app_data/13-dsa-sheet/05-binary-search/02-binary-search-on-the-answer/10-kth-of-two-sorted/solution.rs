// O(log(min(m, n))) time, O(1) space
fn kth_of_two_sorted(a: Vec<i64>, b: Vec<i64>, k: i64) -> i64 {
    let mut a = a;
    let mut b = b;
    if a.len() > b.len() {
        std::mem::swap(&mut a, &mut b);
    }
    let m = a.len();
    let n = b.len();
    let k = k as usize;
    let mut lo = k.saturating_sub(n);
    let mut hi = k.min(m);
    while lo <= hi {
        let i = (lo + hi) / 2;
        let j = k - i;
        let a_left = if i > 0 { a[i - 1] } else { i64::MIN };
        let a_right = if i < m { a[i] } else { i64::MAX };
        let b_left = if j > 0 { b[j - 1] } else { i64::MIN };
        let b_right = if j < n { b[j] } else { i64::MAX };
        if a_left <= b_right && b_left <= a_right {
            return a_left.max(b_left);
        }
        if a_left > b_right {
            hi = i - 1;
        } else {
            lo = i + 1;
        }
    }
    unreachable!()
}

fn main() {
    println!("{:?}", kth_of_two_sorted(vec![2, 3, 6, 7, 9], vec![1, 4, 8, 10], 5));
}
