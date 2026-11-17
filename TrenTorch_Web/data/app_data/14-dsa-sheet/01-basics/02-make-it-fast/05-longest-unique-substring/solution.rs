// O(n) time, O(min(n, charset)) space
fn longest_unique_substring(s: String) -> i64 {
    use std::collections::HashMap;
    let mut last = HashMap::new();
    let mut start = 0usize;
    let mut best = 0usize;
    for (i, ch) in s.chars().enumerate() {
        if let Some(&last_idx) = last.get(&ch) {
            if last_idx >= start {
                start = last_idx + 1;
            }
        }
        last.insert(ch, i);
        let current_len = i - start + 1;
        if current_len > best {
            best = current_len;
        }
    }
    best as i64
}

fn main() {
    println!("{:?}", longest_unique_substring(String::from("abcabcbb")));
}
