use std::collections::VecDeque;

// O(|words| + |stream|) time, O(|words|) space
fn stream_checker(words: Vec<String>, stream: String) -> Vec<bool> {
    // Build trie
    let mut goto = vec![[None; 26]];
    let mut fail = vec![0];
    let mut ends = vec![false];

    for word in words {
        let mut node = 0;
        for ch in word.chars() {
            let idx = (ch as u8 - b'a') as usize;
            let child = goto[node][idx];
            if child.is_none() {
                goto.push([None; 26]);
                fail.push(0);
                ends.push(false);
                let new_node = goto.len() - 1;
                goto[node][idx] = Some(new_node);
                node = new_node;
            } else {
                node = child.unwrap();
            }
        }
        ends[node] = true;
    }

    // Build failure links
    let mut queue = VecDeque::new();
    for idx in 0..26 {
        if let Some(child) = goto[0][idx] {
            fail[child] = 0;
            queue.push_back(child);
        }
    }

    while let Some(node) = queue.pop_front() {
        if ends[fail[node]] {
            ends[node] = true;
        }
        for idx in 0..26 {
            if let Some(child) = goto[node][idx] {
                let mut f = fail[node];
                while f != 0 && goto[f][idx].is_none() {
                    f = fail[f];
                }
                fail[child] = goto[f][idx].unwrap_or(0);
                queue.push_back(child);
            }
        }
    }

    // Process stream
    let mut out = Vec::with_capacity(stream.len());
    let mut state = 0;
    for ch in stream.chars() {
        let idx = (ch as u8 - b'a') as usize;
        while state != 0 && goto[state][idx].is_none() {
            state = fail[state];
        }
        state = goto[state][idx].unwrap_or(0);
        out.push(ends[state]);
    }
    out
}

fn main() {
    println!("{:?}", stream_checker(vec![String::from("cd"), String::from("f"), String::from("kl")], String::from("abcdefghijkl")));
}
