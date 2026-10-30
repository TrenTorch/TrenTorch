// O(n + m) time, O(n + m) space
fn has_cycle_undirected(n: i64, edges: Vec<Vec<i64>>) -> bool {
    let n_usize = n as usize;
    let mut adj: Vec<Vec<(usize, usize)>> = vec![Vec::new(); n_usize];
    for (i, edge) in edges.iter().enumerate() {
        let a = edge[0] as usize;
        let b = edge[1] as usize;
        if a == b {
            return true;
        }
        adj[a].push((b, i));
        adj[b].push((a, i));
    }
    let mut seen = vec![false; n_usize];
    for start in 0..n_usize {
        if seen[start] {
            continue;
        }
        seen[start] = true;
        let mut stack = vec![(start, None)];
        while let Some((node, via)) = stack.pop() {
            for &(nxt, edge_id) in &adj[node] {
                if via == Some(edge_id) {
                    continue;
                }
                if seen[nxt] {
                    return true;
                }
                seen[nxt] = true;
                stack.push((nxt, Some(edge_id)));
            }
        }
    }
    false
}

fn main() {
    println!("{:?}", has_cycle_undirected(4, vec![vec![0, 1], vec![1, 2], vec![2, 0], vec![3, 3]]));
}
