// O(n^2) time, O(n) space
fn min_insertions(s: String) -> i64 {
    let n = s.len();
    if n == 0 {
        return 0;
    }
    let s = s.as_bytes();
    let mut prev = vec![0i64; n];
    for i in (0..n).rev() {
        let mut cur = vec![0i64; n];
        cur[i] = 1;
        for j in (i + 1)..n {
            if s[i] == s[j] {
                cur[j] = 2 + prev[j - 1];
            } else {
                cur[j] = prev[j].max(cur[j - 1]);
            }
        }
        prev = cur;
    }
    n as i64 - prev[n - 1]
}

fn main() {
    println!("{:?}", min_insertions(String::from("mbadm")));
}
