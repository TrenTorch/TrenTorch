use std::collections::HashMap;

// O(n log n) time, O(n) space
fn top_characters(s: &str, k: usize) -> Vec<(char, usize)> {
    let mut counts: HashMap<char, usize> = HashMap::new();
    for ch in s.chars() {
        *counts.entry(ch).or_insert(0) += 1;
    }
    let mut vec: Vec<(char, usize)> = counts.into_iter().collect();
    vec.sort_by(|a, b| {
        b.1.cmp(&a.1).then_with(|| a.0.cmp(&b.0))
    });
    if k < vec.len() {
        vec.truncate(k);
    }
    vec
}

fn main() {
}
