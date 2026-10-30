// O(n + e) time, O(n + e) space
fn valid_path(n: i64, edges: Vec<Vec<i64>>, source: i64, destination: i64) -> bool {
    let n_usize = n as usize;
    let source_usize = source as usize;
    let dest_usize = destination as usize;

    let mut adj = vec![Vec::new(); n_usize];
    for edge in edges {
        let a = edge[0] as usize;
        let b = edge[1] as usize;
        adj[a].push(b);
        adj[b].push(a);
    }

    let mut seen = vec![false; n_usize];
    seen[source_usize] = true;
    let mut stack = vec![source_usize];

    while let Some(node) = stack.pop() {
        if node == dest_usize {
            return true;
        }
        for &nxt in &adj[node] {
            if !seen[nxt] {
                seen[nxt] = true;
                stack.push(nxt);
            }
        }
    }
    false
}

fn main() {
    println!("{:?}", valid_path(3, vec![vec![0, 1], vec![1, 2], vec![2, 0]], 0, 2));
}
