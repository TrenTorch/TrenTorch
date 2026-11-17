use std::collections::HashSet;

// O(n) time (plus sorting the repeated set), O(n) space
fn repeated_dna(s: String) -> Vec<String> {
    let mut seen: HashSet<&str> = HashSet::new();
    let mut repeated: HashSet<&str> = HashSet::new();
    if s.len() >= 10 {
        for i in 0..=(s.len() - 10) {
            let part = &s[i..i + 10];
            if !seen.insert(part) {
                repeated.insert(part);
            }
        }
    }
    let mut out: Vec<String> = repeated.into_iter().map(|p| p.to_string()).collect();
    out.sort();
    out
}

fn main() {
    println!("{:?}", repeated_dna(String::from("AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT")));
}
