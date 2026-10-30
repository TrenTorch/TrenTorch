use std::collections::{HashMap, HashSet};

fn longest_word(words: Vec<String>) -> String {
    // O(N * L) time, O(N) space where N = number of words, L = max word length (<=30)
    let unique_words: HashSet<String> = words.into_iter().collect();
    let mut by_length: HashMap<usize, Vec<String>> = HashMap::new();
    for word in unique_words {
        by_length.entry(word.len()).or_default().push(word);
    }
    let mut built: HashSet<String> = HashSet::new();
    built.insert(String::new());
    let mut best = String::new();
    let mut length = 1;
    loop {
        let words_of_len = match by_length.remove(&length) {
            Some(v) => v,
            None => return best,
        };
        let mut good = Vec::new();
        for word in words_of_len {
            let prefix = &word[..word.len() - 1];
            if built.contains(prefix) {
                good.push(word);
            }
        }
        if good.is_empty() {
            return best;
        }
        let min_word = good.iter().min().unwrap().clone();
        built.extend(good);
        best = min_word;
        length += 1;
    }
}

fn main() {
    println!("{:?}", longest_word(vec![String::from("w"), String::from("wo"), String::from("wor"), String::from("worl"), String::from("world")]));
}
