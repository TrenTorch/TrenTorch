// O(n + m) time, O(1) space
fn is_subsequence(s: String, t: String) -> bool {
    let s_bytes = s.as_bytes();
    let t_bytes = t.as_bytes();
    let mut i = 0;
    for &ch in t_bytes {
        if i < s_bytes.len() && s_bytes[i] == ch {
            i += 1;
        }
    }
    i == s_bytes.len()
}

fn main() {
    println!("{:?}", is_subsequence(String::from("ace"), String::from("abcde")));
}
