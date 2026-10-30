// O(n) time, O(n) space (suffix automaton with 26-letter transitions)
fn longest_repeated_length(s: String) -> i64 {
    let bytes = s.as_bytes();
    let n = bytes.len();
    let mut nxt: Vec<[i64; 26]> = vec![[-1; 26]];
    let mut link: Vec<i64> = vec![-1];
    let mut length: Vec<i64> = vec![0];
    let mut occ: Vec<i64> = vec![0];
    let mut last: usize = 0;
    for &b in bytes {
        let c = (b - b'a') as usize;
        let cur = nxt.len();
        nxt.push([-1; 26]);
        link.push(0);
        length.push(length[last] + 1);
        occ.push(1);
        let mut p: i64 = last as i64;
        while p != -1 && nxt[p as usize][c] == -1 {
            nxt[p as usize][c] = cur as i64;
            p = link[p as usize];
        }
        if p != -1 {
            let q = nxt[p as usize][c] as usize;
            if length[p as usize] + 1 == length[q] {
                link[cur] = q as i64;
            } else {
                let clone = nxt.len();
                let q_next = nxt[q];
                nxt.push(q_next);
                link.push(link[q]);
                length.push(length[p as usize] + 1);
                occ.push(0);
                while p != -1 && nxt[p as usize][c] == q as i64 {
                    nxt[p as usize][c] = clone as i64;
                    p = link[p as usize];
                }
                link[q] = clone as i64;
                link[cur] = clone as i64;
            }
        }
        last = cur;
    }

    let mut by_length: Vec<Vec<usize>> = vec![Vec::new(); n + 1];
    for v in 1..nxt.len() {
        by_length[length[v] as usize].push(v);
    }
    let mut best: i64 = 0;
    for size in (1..=n).rev() {
        for &v in &by_length[size] {
            if occ[v] >= 2 {
                best = best.max(size as i64);
            }
            let l = link[v] as usize;
            occ[l] += occ[v];
        }
    }
    best
}

fn main() {
    println!("{:?}", longest_repeated_length(String::from("banana")));
}
