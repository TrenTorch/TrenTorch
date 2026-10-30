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

// O(n * L) time where L is the longest word (<= 10), O(total characters in words) space
fn index_pairs(text: String, words: Vec<String>) -> Vec<Vec<i64>> {
    let mut nodes: Vec<TrieNode> = vec![TrieNode::new()];
    for word in &words {
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

    let text = text.into_bytes();
    let n = text.len();
    let mut out: Vec<Vec<i64>> = Vec::new();
    for i in 0..n {
        let mut cur = 0usize;
        for j in i..n {
            let idx = match text[j] {
                b'a'..=b'z' => (text[j] - b'a') as usize,
                _ => break,
            };
            match nodes[cur].children[idx] {
                Some(next) => cur = next,
                None => break,
            }
            if nodes[cur].is_end {
                out.push(vec![i as i64, j as i64]);
            }
        }
    }
    out
}

fn main() {
    println!("{:?}", index_pairs(String::from("thestoryofleetcodeandme"), vec![String::from("story"), String::from("fleet"), String::from("leetcode")]));
}
