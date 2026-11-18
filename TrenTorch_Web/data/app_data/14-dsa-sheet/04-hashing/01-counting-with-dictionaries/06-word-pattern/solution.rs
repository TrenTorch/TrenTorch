use std::collections::HashMap;

// O(n) time, O(n) space
fn word_pattern(pattern: String, words: Vec<String>) -> bool {
    if pattern.len() != words.len() {
        return false;
    }
    let mut letter_to_word: HashMap<char, String> = HashMap::new();
    let mut word_to_letter: HashMap<String, char> = HashMap::new();

    for (c, w) in pattern.chars().zip(words.iter()) {
        let entry = letter_to_word.entry(c).or_insert_with(|| w.clone());
        if entry != w {
            return false;
        }
        let entry2 = word_to_letter.entry(w.clone()).or_insert(c);
        if *entry2 != c {
            return false;
        }
    }
    true
}

fn main() {
    println!("{:?}", word_pattern(
        String::from("abba"),
        vec![
            String::from("dog"),
            String::from("cat"),
            String::from("cat"),
            String::from("dog")
        ]
    ));
}
