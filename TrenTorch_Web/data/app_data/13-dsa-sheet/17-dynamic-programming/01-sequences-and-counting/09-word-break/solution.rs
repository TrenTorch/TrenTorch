struct TrieNode {
    children: [Option<Box<TrieNode>>; 26],
    is_end: bool,
}

impl TrieNode {
    fn new() -> Self {
        TrieNode {
            children: Default::default(),
            is_end: false,
        }
    }
}

// O(n * L) time, O(n + total_chars) space where L is max word length (<=20)
fn word_break(s: String, words: Vec<String>) -> bool {
    let mut root = TrieNode::new();
    for word in words {
        let mut node = &mut root;
        for ch in word.bytes() {
            let idx = (ch - b'a') as usize;
            node = node.children[idx].get_or_insert_with(|| Box::new(TrieNode::new()));
        }
        node.is_end = true;
    }

    let n = s.len();
    let mut reachable = vec![false; n + 1];
    reachable[0] = true;
    let s_bytes = s.as_bytes();

    for i in 0..n {
        if !reachable[i] {
            continue;
        }
        let mut node = &root;
        for j in i..n {
            let idx = (s_bytes[j] - b'a') as usize;
            match &node.children[idx] {
                Some(child) => {
                    node = child.as_ref();
                    if node.is_end {
                        reachable[j + 1] = true;
                    }
                }
                None => break,
            }
        }
    }

    reachable[n]
}

fn main() {
    println!("{:?}", word_break(String::from("leetcode"), vec![String::from("leet"), String::from("code")]));
}
