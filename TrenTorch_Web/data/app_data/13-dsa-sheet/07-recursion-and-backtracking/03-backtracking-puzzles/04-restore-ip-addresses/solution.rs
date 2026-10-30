// O(1) time and O(1) extra space for the fixed 4-part search (at most 3^4 splits)
fn restore_ip_addresses(s: String) -> Vec<String> {
    let mut out: Vec<String> = Vec::new();
    let mut parts: Vec<String> = Vec::new();
    ip_go(&s, 0, &mut parts, &mut out);
    out.sort();
    out
}

fn valid_ip_part(part: &str) -> bool {
    (part == "0" || !part.starts_with('0')) && part.parse::<i64>().map_or(false, |v| v <= 255)
}

fn ip_go(s: &str, start: usize, parts: &mut Vec<String>, out: &mut Vec<String>) {
    if parts.len() == 4 {
        if start == s.len() {
            out.push(parts.join("."));
        }
        return;
    }
    for length in 1..=3 {
        if start + length > s.len() {
            continue;
        }
        let part = &s[start..start + length];
        if valid_ip_part(part) {
            parts.push(part.to_string());
            ip_go(s, start + length, parts, out);
            parts.pop();
        }
    }
}

fn main() {
    println!("{:?}", restore_ip_addresses(String::from("25525511135")));
}
