// O(n + m) time, O(n + m) space
fn has_cycle_directed(n: i64, edges: Vec<Vec<i64>>) -> bool {
    let n = n as usize;
    let mut adj = vec![Vec::new(); n];
    for e in edges {
        let a = e[0] as usize;
        let b = e[1] as usize;
        adj[a].push(b);
    }
    let mut state = vec![0u8; n]; // 0 = unvisited, 1 = visiting, 2 = visited
    for start in 0..n {
        if state[start] != 0 {
            continue;
        }
        state[start] = 1;
        let mut stack = Vec::new();
        stack.push((start, 0));
        while let Some((node, i)) = stack.pop() {
            if i < adj[node].len() {
                stack.push((node, i + 1));
                let nxt = adj[node][i];
                if state[nxt] == 1 {
                    return true;
                }
                if state[nxt] == 0 {
                    state[nxt] = 1;
                    stack.push((nxt, 0));
                }
            } else {
                state[node] = 2;
            }
        }
    }
    false
}

fn main() {
    println!("{:?}", has_cycle_directed(3, vec![vec![0, 1], vec![1, 2], vec![2, 0]]));
}
