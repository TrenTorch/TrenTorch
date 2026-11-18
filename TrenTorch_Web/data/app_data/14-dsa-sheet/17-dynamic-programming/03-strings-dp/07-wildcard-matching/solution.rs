// O(n*m) time, O(m) space where n = s.len(), m = p.len()
fn is_match_wildcard(s: String, p: String) -> bool {
    let s_bytes = s.as_bytes();
    let p_bytes = p.as_bytes();
    let n = s_bytes.len();
    let m = p_bytes.len();

    let mut prev = vec![false; m + 1];
    prev[0] = true;
    for j in 1..=m {
        prev[j] = prev[j - 1] && p_bytes[j - 1] == b'*';
    }

    for i in 1..=n {
        let mut cur = vec![false; m + 1];
        for j in 1..=m {
            if p_bytes[j - 1] == b'*' {
                cur[j] = cur[j - 1] || prev[j];
            } else if p_bytes[j - 1] == b'?' || p_bytes[j - 1] == s_bytes[i - 1] {
                cur[j] = prev[j - 1];
            }
        }
        prev = cur;
    }

    prev[m]
}

fn main() {
    println!("{:?}", is_match_wildcard(String::from("aa"), String::from("*")));
}
