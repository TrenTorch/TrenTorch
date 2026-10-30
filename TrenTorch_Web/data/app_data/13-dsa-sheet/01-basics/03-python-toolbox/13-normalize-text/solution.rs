// O(n) time, O(n) space
fn normalize_text(s: String) -> String {
    let mut res = String::with_capacity(s.len());
    for byte in s.bytes() {
        let ch = (byte as char).to_ascii_lowercase();
        if ch.is_ascii_alphanumeric() {
            res.push(ch);
        } else if !res.is_empty() && !res.ends_with(' ') {
            res.push(' ');
        }
    }
    if res.ends_with(' ') {
        res.pop();
    }
    res
}

fn main() {
    println!("{:?}", normalize_text(String::from("  Hello,   World!! 42 ")));
}
