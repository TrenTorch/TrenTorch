// O(N * L + Q * L) time, O(N * L) space where N = number of words, Q = number of queries, L = max word length (<=12)
struct TrieNode {
    count: i64,
    children: [Option<Box<TrieNode>>; 26],
}

impl TrieNode {
    fn new() -> Self {
        TrieNode {
            count: 0,
            children: std::array::from_fn(|_| None),
        }
    }
}

fn count_with_prefix(words: Vec<String>, queries: Vec<String>) -> Vec<i64> {
    let mut root = TrieNode::new();
    // Build trie
    for word in words {
        let mut node = &mut root;
        for ch in word.chars() {
            let idx = (ch as u8 - b'a') as usize;
            if node.children[idx].is_none() {
                node.children[idx] = Some(Box::new(TrieNode::new()));
            }
            node = node.children[idx].as_mut().unwrap();
            node.count += 1;
        }
    }
    // Answer queries
    let mut out = Vec::with_capacity(queries.len());
    for query in queries {
        let mut node: Option<&TrieNode> = Some(&root);
        for ch in query.chars() {
            let idx = (ch as u8 - b'a') as usize;
            node = match node {
                Some(n) => n.children[idx].as_deref(),
                None => None,
            };
            if node.is_none() {
                break;
            }
        }
        out.push(node.map_or(0, |n| n.count));
    }
    out
}

fn main() {
    println!("{:?}", count_with_prefix(vec![String::from("apple"), String::from("app"), String::from("apt"), String::from("bat")], vec![String::from("ap"), String::from("app"), String::from("b"), String::from("c")]));
}
