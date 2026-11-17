use std::collections::HashMap;

// O(n) time, O(1) space (at most 26 distinct letters)
fn least_interval(tasks: String, n: i64) -> i64 {
    if tasks.is_empty() {
        return 0;
    }
    let mut counts: HashMap<char, i64> = HashMap::new();
    for t in tasks.chars() {
        *counts.entry(t).or_insert(0) += 1;
    }
    let m = *counts.values().max().unwrap();
    let ties = counts.values().filter(|&&c| c == m).count() as i64;
    let len = tasks.chars().count() as i64;
    len.max((m - 1) * (n + 1) + ties)
}

fn main() {
    println!("{:?}", least_interval(String::from("AAABBB"), 2));
}
