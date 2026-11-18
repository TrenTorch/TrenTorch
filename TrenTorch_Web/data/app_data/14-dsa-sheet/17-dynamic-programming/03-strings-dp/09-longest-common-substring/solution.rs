use std::collections::HashMap;

// O(|a| + |b|) time, O(|a|) space
fn longest_common_substring(a: String, b: String) -> i64 {
    let mut nxt = vec![HashMap::new()];
    let mut link = vec![-1];
    let mut length = vec![0];
    let mut last = 0usize;

    for ch in a.chars() {
        let cur = nxt.len();
        nxt.push(HashMap::new());
        length.push(length[last] + 1);
        link.push(0); // placeholder
        let mut p = last as i64;
        while p != -1 && !nxt[p as usize].contains_key(&ch) {
            nxt[p as usize].insert(ch, cur);
            p = link[p as usize];
        }
        if p != -1 {
            let q = nxt[p as usize][&ch];
            if length[p as usize] + 1 == length[q] {
                link[cur] = q as i64;
            } else {
                let clone = nxt.len();
                nxt.push(nxt[q].clone());
                length.push(length[p as usize] + 1);
                link.push(link[q]);
                while p != -1 && nxt[p as usize].get(&ch) == Some(&q) {
                    nxt[p as usize].insert(ch, clone);
                    p = link[p as usize];
                }
                link[q] = clone as i64;
                link[cur] = clone as i64;
            }
        }
        last = cur;
    }

    let mut best = 0i64;
    let mut match_len = 0i64;
    let mut state = 0usize;

    for ch in b.chars() {
        while state != 0 && !nxt[state].contains_key(&ch) {
            state = link[state] as usize;
            match_len = length[state];
        }
        if nxt[state].contains_key(&ch) {
            state = nxt[state][&ch];
            match_len += 1;
        } else {
            state = 0;
            match_len = 0;
        }
        if match_len > best {
            best = match_len;
        }
    }
    best
}

fn main() {
    println!("{:?}", longest_common_substring(String::from("abcdxyz"), String::from("xyzabcd")));
}
