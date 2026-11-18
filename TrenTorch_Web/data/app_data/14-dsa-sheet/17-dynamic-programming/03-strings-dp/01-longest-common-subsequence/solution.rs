// O(n*m) time, O(min(n,m)) space
fn lcs_length(a: String, b: String) -> i64 {
    let (a, b) = if b.len() > a.len() { (b, a) } else { (a, b) };
    let a_chars: Vec<char> = a.chars().collect();
    let b_chars: Vec<char> = b.chars().collect();
    let n = a_chars.len();
    let m = b_chars.len();
    let mut prev = vec![0i64; m + 1];
    for i in 1..=n {
        let mut cur = vec![0i64; m + 1];
        for j in 1..=m {
            if a_chars[i - 1] == b_chars[j - 1] {
                cur[j] = prev[j - 1] + 1;
            } else {
                cur[j] = std::cmp::max(prev[j], cur[j - 1]);
            }
        }
        prev = cur;
    }
    prev[m]
}

fn main() {
    println!("{:?}", lcs_length(String::from("abcde"), String::from("ace")));
}
