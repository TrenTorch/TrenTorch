use std::collections::{HashMap, HashSet, VecDeque};

fn pattern(word: &str, i: usize) -> String {
    let mut s = String::with_capacity(word.len());
    s.push_str(&word[..i]);
    s.push('*');
    s.push_str(&word[i + 1..]);
    s
}

// O(N * L^2) time, O(N * L^2) space (N words of length L; each wildcard pattern has length L)
fn ladder_length(begin: String, end: String, words: Vec<String>) -> i64 {
    let allowed: HashSet<String> = words.into_iter().collect();
    if !allowed.contains(&end) {
        return 0;
    }
    let mut all = allowed;
    all.insert(begin.clone());
    let mut groups: HashMap<String, Vec<String>> = HashMap::new();
    for word in &all {
        for i in 0..word.len() {
            let key = pattern(word, i);
            groups.entry(key).or_insert_with(Vec::new).push(word.clone());
        }
    }
    let mut seen: HashSet<String> = HashSet::new();
    seen.insert(begin.clone());
    let mut queue: VecDeque<(String, i64)> = VecDeque::new();
    queue.push_back((begin, 1));
    while let Some((word, steps)) = queue.pop_front() {
        if word == end {
            return steps;
        }
        for i in 0..word.len() {
            let key = pattern(&word, i);
            if let Some(list) = groups.get(&key) {
                for other in list {
                    if !seen.contains(other) {
                        seen.insert(other.clone());
                        queue.push_back((other.clone(), steps + 1));
                    }
                }
            }
        }
    }
    0
}

fn main() {
    println!("{:?}", ladder_length(String::from("hit"), String::from("cog"), vec![String::from("hot"), String::from("dot"), String::from("dog"), String::from("lot"), String::from("log"), String::from("cog")]));
}
