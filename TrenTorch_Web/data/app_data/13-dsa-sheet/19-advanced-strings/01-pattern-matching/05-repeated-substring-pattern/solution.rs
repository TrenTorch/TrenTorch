// O(n) time, O(n) space
fn repeated_substring_pattern(s: String) -> bool {
    let s = s.into_bytes();
    let n = s.len();
    if n < 2 {
        return false;
    }
    let mut pi = vec![0usize; n];
    let mut k = 0usize;
    for i in 1..n {
        while k > 0 && s[i] != s[k] {
            k = pi[k - 1];
        }
        if s[i] == s[k] {
            k += 1;
        }
        pi[i] = k;
    }
    let last = pi[n - 1];
    let period = n - last;
    last > 0 && n % period == 0
}

fn main() {
    println!("{:?}", repeated_substring_pattern(String::from("abab")));
}
