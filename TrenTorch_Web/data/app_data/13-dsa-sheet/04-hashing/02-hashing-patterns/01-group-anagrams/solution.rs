use std::collections::HashMap;

// O(n * L log L) time, O(n) space
fn group_anagrams(words: Vec<String>) -> Vec<Vec<String>> {
    let mut map: HashMap<String, Vec<String>> = HashMap::new();
    for word in words {
        let mut chars: Vec<char> = word.chars().collect();
        chars.sort_unstable();
        let key: String = chars.iter().collect();
        map.entry(key).or_default().push(word);
    }
    let mut groups: Vec<Vec<String>> = map.into_values().collect();
    for group in groups.iter_mut() {
        group.sort();
    }
    groups.sort_by(|a, b| a[0].cmp(&b[0]));
    groups
}

fn main() {
    println!("{:?}", group_anagrams(vec![
        String::from("eat"),
        String::from("tea"),
        String::from("tan"),
        String::from("ate"),
        String::from("nat"),
        String::from("bat")
    ]));
}
