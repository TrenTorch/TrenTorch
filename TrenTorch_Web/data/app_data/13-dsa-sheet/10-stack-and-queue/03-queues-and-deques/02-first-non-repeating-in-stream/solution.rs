use std::collections::{HashMap, VecDeque};

// O(n) time, O(n) space
fn first_non_repeating_stream(s: String) -> String {
    let mut counts: HashMap<char, usize> = HashMap::new();
    let mut queue: VecDeque<char> = VecDeque::new();
    let mut out = String::with_capacity(s.len());
    for ch in s.chars() {
        let c = counts.entry(ch).or_insert(0);
        *c += 1;
        let count_now = *c;
        if count_now == 1 {
            queue.push_back(ch);
        }
        while let Some(&front) = queue.front() {
            if counts[&front] > 1 {
                queue.pop_front();
            } else {
                break;
            }
        }
        match queue.front() {
            Some(&f) => out.push(f),
            None => out.push('#'),
        }
    }
    out
}

fn main() {
    println!("{:?}", first_non_repeating_stream(String::from("aabc")));
}
