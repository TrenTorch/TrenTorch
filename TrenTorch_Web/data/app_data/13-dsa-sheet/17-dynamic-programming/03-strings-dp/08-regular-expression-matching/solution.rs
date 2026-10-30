fn is_match_regex(s: String, p: String) -> bool {
    // O(n*m) time, O(m) space where n = s.len(), m = p.len()
    let s_chars: Vec<char> = s.chars().collect();
    let p_chars: Vec<char> = p.chars().collect();
    let n = s_chars.len();
    let m = p_chars.len();

    let fits = |x: char, ch: char| -> bool { x == '.' || x == ch };

    let mut prev = vec![false; m + 1];
    prev[0] = true;
    for j in 2..=m {
        if p_chars[j - 1] == '*' {
            prev[j] = prev[j - 2];
        }
    }

    for i in 1..=n {
        let mut cur = vec![false; m + 1];
        for j in 1..=m {
            if p_chars[j - 1] == '*' {
                cur[j] = cur[j - 2] || (fits(p_chars[j - 2], s_chars[i - 1]) && prev[j]);
            } else {
                cur[j] = fits(p_chars[j - 1], s_chars[i - 1]) && prev[j - 1];
            }
        }
        prev = cur;
    }

    prev[m]
}

fn main() {
    println!("{:?}", is_match_regex(String::from("aab"), String::from("c*a*b")));
}
