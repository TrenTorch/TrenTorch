// O(n + m) time, O(n + m) space
fn count_scc(n: i64, edges: Vec<Vec<i64>>) -> i64 {
    let n_usize = n as usize;
    let mut adj = vec![Vec::new(); n_usize];
    let mut rev = vec![Vec::new(); n_usize];
    for edge in edges {
        let a = edge[0] as usize;
        let b = edge[1] as usize;
        adj[a].push(b);
        rev[b].push(a);
    }
    let mut seen = vec![false; n_usize];
    let mut order = Vec::with_capacity(n_usize);
    for start in 0..n_usize {
        if seen[start] {
            continue;
        }
        seen[start] = true;
        let mut stack = vec![(start, 0)];
        while let Some((node, i)) = stack.pop() {
            if i < adj[node].len() {
                stack.push((node, i + 1));
                let nxt = adj[node][i];
                if !seen[nxt] {
                    seen[nxt] = true;
                    stack.push((nxt, 0));
                }
            } else {
                order.push(node);
            }
        }
    }
    seen = vec![false; n_usize];
    let mut count = 0;
    for &start in order.iter().rev() {
        if seen[start] {
            continue;
        }
        count += 1;
        seen[start] = true;
        let mut stack = vec![start];
        while let Some(node) = stack.pop() {
            for &nxt in &rev[node] {
                if !seen[nxt] {
                    seen[nxt] = true;
                    stack.push(nxt);
                }
            }
        }
    }
    count as i64
}

fn main() {
    println!("{:?}", count_scc(5, vec![vec![0, 1], vec![1, 2], vec![2, 0], vec![1, 3], vec![3, 4]]));
}
