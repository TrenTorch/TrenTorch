fn shortest_palindrome(s: String) -> String {
    // O(n) time, O(n) space
    let s_bytes = s.as_bytes();
    let n = s_bytes.len();
    if n == 0 {
        return String::new();
    }
    let mut t = Vec::with_capacity(2 * n + 1);
    t.extend_from_slice(s_bytes);
    t.push(b'#');
    t.extend(s_bytes.iter().rev());

    let mut pi = vec![0; t.len()];
    let mut k = 0;
    for i in 1..t.len() {
        while k > 0 && t[i] != t[k] {
            k = pi[k - 1];
        }
        if t[i] == t[k] {
            k += 1;
        }
        pi[i] = k;
    }

    let border = *pi.last().unwrap_or(&0);
    let suffix = &s[border..];
    let mut result = String::with_capacity(suffix.len() + n);
    result.extend(suffix.chars().rev());
    result.push_str(&s);
    result
}

fn main() {
    println!("{:?}", shortest_palindrome(String::from("aacecaaa")));
}
