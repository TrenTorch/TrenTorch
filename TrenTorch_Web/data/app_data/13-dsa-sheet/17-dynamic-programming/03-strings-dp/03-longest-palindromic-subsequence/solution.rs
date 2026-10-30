// O(n^2) time, O(n) space
fn longest_palindrome_subseq(s: String) -> i64 {
    let s = s.into_bytes();
    let n = s.len();
    if n == 0 {
        return 0;
    }
    let mut prev = vec![0i64; n];
    for i in (0..n).rev() {
        let mut cur = vec![0i64; n];
        cur[i] = 1;
        for j in (i + 1)..n {
            cur[j] = if s[i] == s[j] {
                2 + prev[j - 1]
            } else {
                std::cmp::max(prev[j], cur[j - 1])
            };
        }
        prev = cur;
    }
    prev[n - 1]
}

fn main() {
    println!("{:?}", longest_palindrome_subseq(String::from("bbbab")));
}
