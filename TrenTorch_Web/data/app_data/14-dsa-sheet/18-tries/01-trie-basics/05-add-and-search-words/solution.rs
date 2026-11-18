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

fn matches(nodes: &[TrieNode], node: usize, pat: &[u8], i: usize) -> bool {
    if i == pat.len() {
        return nodes[node].is_end;
    }
    let ch = pat[i];
    if ch == b'.' {
        for child in nodes[node].children.iter() {
            if let Some(next) = *child {
                if matches(nodes, next, pat, i + 1) {
                    return true;
                }
            }
        }
        false
    } else {
        let idx = (ch - b'a') as usize;
        match nodes[node].children[idx] {
            Some(next) => matches(nodes, next, pat, i + 1),
            None => false,
        }
    }
}

// O(total characters) time for add, O(26^L) worst case per search with '.' patterns, O(total characters) space
fn run_word_dictionary(ops: Vec<String>) -> Vec<bool> {
    let mut nodes: Vec<TrieNode> = vec![TrieNode::new()];
    let mut out = Vec::new();
    for op in ops {
        let mut parts = op.split_whitespace();
        let kind = parts.next().unwrap_or("");
        let text = parts.next().unwrap_or("");
        if kind == "add" {
            let mut cur = 0usize;
            for ch in text.bytes() {
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
        } else {
            out.push(matches(&nodes, 0, text.as_bytes(), 0));
        }
    }
    out
}

fn main() {
    println!("{:?}", run_word_dictionary(vec![String::from("add bad"), String::from("add dad"), String::from("add mad"), String::from("search pad"), String::from("search bad"), String::from("search .ad"), String::from("search b..")]));
}
