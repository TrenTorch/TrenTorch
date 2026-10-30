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

// O(total root characters + total sentence characters) time, O(total root characters) space
fn replace_words(roots: Vec<String>, sentence: String) -> String {
    let mut nodes: Vec<TrieNode> = vec![TrieNode::new()];
    for root in &roots {
        let mut cur = 0usize;
        for ch in root.bytes() {
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

    let mut out: Vec<String> = Vec::new();
    for word in sentence.split_whitespace() {
        let mut cur = 0usize;
        let mut replace_len: Option<usize> = None;
        for (i, ch) in word.bytes().enumerate() {
            let idx = (ch - b'a') as usize;
            match nodes[cur].children[idx] {
                Some(next) => cur = next,
                None => break,
            }
            if nodes[cur].is_end {
                replace_len = Some(i + 1);
                break;
            }
        }
        match replace_len {
            Some(len) => out.push(word[..len].to_string()),
            None => out.push(word.to_string()),
        }
    }
    out.join(" ")
}

fn main() {
    println!("{:?}", replace_words(vec![String::from("cat"), String::from("bat"), String::from("rat")], String::from("the cattle was rattled by the battery")));
}
