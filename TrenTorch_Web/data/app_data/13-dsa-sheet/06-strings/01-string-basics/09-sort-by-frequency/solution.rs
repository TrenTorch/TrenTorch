use std::collections::HashMap;

// O(n log n) time, O(n) space
fn sort_by_frequency(s: String) -> String {
    let mut counts: HashMap<char, usize> = HashMap::new();
    for ch in s.chars() {
        *counts.entry(ch).or_insert(0) += 1;
    }

    let mut chars: Vec<char> = counts.keys().cloned().collect();
    chars.sort_by(|&a, &b| {
        let ca = counts.get(&a).unwrap();
        let cb = counts.get(&b).unwrap();
        match cb.cmp(ca) {
            std::cmp::Ordering::Equal => a.cmp(&b),
            other => other,
        }
    });

    let mut result = String::with_capacity(s.len());
    for ch in chars {
        let cnt = counts.get(&ch).unwrap();
        for _ in 0..*cnt {
            result.push(ch);
        }
    }
    result
}

fn main() {
    println!("{:?}", sort_by_frequency(String::from("tree")));
}
