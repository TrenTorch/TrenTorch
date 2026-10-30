struct TrieNode {
    children: [Option<usize>; 26],
    is_end: bool,
}

impl TrieNode {
    fn new() -> Self {
        TrieNode {
            children: [None; 26],
            is_end: false,
        }
    }
}

fn walk(nodes: &[TrieNode], word: &str) -> Option<usize> {
    let mut cur = 0usize;
    for ch in word.bytes() {
        let idx = (ch - b'a') as usize;
        match nodes[cur].children[idx] {
            Some(next) => cur = next,
            None => return None,
        }
    }
    Some(cur)
}

// O(total characters) time, O(total characters) space
fn run_trie(ops: Vec<String>) -> Vec<bool> {
    let mut nodes: Vec<TrieNode> = vec![TrieNode::new()];
    let mut out = Vec::new();
    for op in ops {
        let mut parts = op.split_whitespace();
        let kind = parts.next().unwrap_or("");
        let word = parts.next().unwrap_or("");
        match kind {
            "insert" => {
                let mut cur = 0usize;
                for ch in word.bytes() {
                    let idx = (ch - b'a') as usize;
                    let existing = nodes[cur].children[idx];
                    cur = match existing {
                        Some(next) => next,
                        None => {
                            nodes.push(TrieNode::new());
                            let new_idx = nodes.len() - 1;
                            nodes[cur].children[idx] = Some(new_idx);
                            new_idx
                        }
                    };
                }
                nodes[cur].is_end = true;
            }
            "search" => {
                let found = match walk(&nodes, word) {
                    Some(node) => nodes[node].is_end,
                    None => false,
                };
                out.push(found);
            }
            _ => {
                out.push(walk(&nodes, word).is_some());
            }
        }
    }
    out
}

fn main() {
    println!("{:?}", run_trie(vec![String::from("insert apple"), String::from("search apple"), String::from("search app"), String::from("starts app"), String::from("insert app"), String::from("search app")]));
}
