// O(n * L) time, O(1) extra space
fn longest_common_prefix(words: Vec<String>) -> String {
    if words.is_empty() {
        return String::new();
    }
    let min_word = words.iter().min().unwrap();
    let max_word = words.iter().max().unwrap();

    let mut i = 0;
    let limit = std::cmp::min(min_word.len(), max_word.len());
    let min_bytes = min_word.as_bytes();
    let max_bytes = max_word.as_bytes();

    while i < limit && min_bytes[i] == max_bytes[i] {
        i += 1;
    }
    min_word[..i].to_string()
}

fn main() {
    println!("{:?}", longest_common_prefix(vec![String::from("flower"), String::from("flow"), String::from("flight")]));
}
