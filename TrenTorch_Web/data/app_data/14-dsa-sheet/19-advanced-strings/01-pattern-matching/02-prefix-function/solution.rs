// O(n) time, O(n) space
fn prefix_function(s: String) -> Vec<i64> {
    let chars: Vec<char> = s.chars().collect();
    let n = chars.len();
    let mut pi = vec![0i64; n];
    let mut k = 0usize;
    for i in 1..n {
        while k > 0 && chars[i] != chars[k] {
            k = pi[k - 1] as usize;
        }
        if chars[i] == chars[k] {
            k += 1;
        }
        pi[i] = k as i64;
    }
    pi
}

fn main() {
    println!("{:?}", prefix_function(String::from("abcabca")));
}
