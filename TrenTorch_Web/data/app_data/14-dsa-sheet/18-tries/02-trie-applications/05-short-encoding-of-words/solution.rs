use std::collections::{HashMap, HashSet};

struct TrieNode {
    children: HashMap<char, usize>,
}

// O(N * L) time, O(N * L) space where N is number of unique words, L is max word length.
fn minimum_length_encoding(words: Vec<String>) -> i64 {
    let unique_words: HashSet<String> = words.into_iter().collect();
    
    let mut nodes = Vec::new();
    nodes.push(TrieNode { children: HashMap::new() }); // root at index 0
    let mut ends = Vec::new();
    
    for word in unique_words {
        let mut node_idx = 0;
        for ch in word.chars().rev() {
            // Check if child exists using immutable reference
            let child_idx = {
                let node = &nodes[node_idx];
                node.children.get(&ch).copied()
            };
            if let Some(child_idx) = child_idx {
                node_idx = child_idx;
            } else {
                let new_idx = nodes.len();
                nodes.push(TrieNode { children: HashMap::new() });
                let node = &mut nodes[node_idx];
                node.children.insert(ch, new_idx);
                node_idx = new_idx;
            }
        }
        ends.push((node_idx, word.len()));
    }
    
    let mut total = 0;
    for (idx, len) in ends {
        if nodes[idx].children.is_empty() {
            total += len as i64 + 1;
        }
    }
    total
}

fn main() {
    println!("{:?}", minimum_length_encoding(vec![String::from("time"), String::from("me"), String::from("bell")]));
}
