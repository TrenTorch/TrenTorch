use std::collections::{HashMap, HashSet};

fn is_palindrome(s: &str) -> bool {
    let chars: Vec<char> = s.chars().collect();
    let len = chars.len();
    for i in 0..len / 2 {
        if chars[i] != chars[len - 1 - i] {
            return false;
        }
    }
    true
}

// O(n * k^2) time, O(n * k) space where n is number of words, k is max word length
fn palindrome_pairs(words: Vec<String>) -> Vec<Vec<i64>> {
    let mut index: HashMap<String, Vec<i64>> = HashMap::new();
    for (i, word) in words.iter().enumerate() {
        index.entry(word.clone()).or_default().push(i as i64);
    }

    let mut found = HashSet::new();

    for (i, word) in words.iter().enumerate() {
        let i = i as i64;
        let len = word.len();
        for cut in 0..=len {
            let prefix = &word[..cut];
            let suffix = &word[cut..];

            if is_palindrome(prefix) {
                let rev_suffix: String = suffix.chars().rev().collect();
                if let Some(indices) = index.get(&rev_suffix) {
                    for &j in indices {
                        if j != i {
                            found.insert((j, i));
                        }
                    }
                }
            }

            if is_palindrome(suffix) {
                let rev_prefix: String = prefix.chars().rev().collect();
                if let Some(indices) = index.get(&rev_prefix) {
                    for &j in indices {
                        if j != i {
                            found.insert((i, j));
                        }
                    }
                }
            }
        }
    }

    let mut result: Vec<Vec<i64>> = found.into_iter().map(|(a, b)| vec![a, b]).collect();
    result.sort();
    result
}

fn main() {
    println!("{:?}", palindrome_pairs(vec![String::from("abcd"), String::from("dcba"), String::from("lls"), String::from("s"), String::from("sssll")]));
}
