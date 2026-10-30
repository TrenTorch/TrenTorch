// O(n + m) time, O(n + m) space
fn is_bipartite(n: i64, edges: Vec<Vec<i64>>) -> bool {
    let n_usize = n as usize;
    let mut adj = vec![Vec::new(); n_usize];
    for edge in edges {
        let a = edge[0] as usize;
        let b = edge[1] as usize;
        adj[a].push(b);
        adj[b].push(a);
    }
    let mut color = vec![-1; n_usize];
    let mut queue = std::collections::VecDeque::new();
    for start in 0..n_usize {
        if color[start] != -1 {
            continue;
        }
        color[start] = 0;
        queue.push_back(start);
        while let Some(node) = queue.pop_front() {
            for &nxt in &adj[node] {
                if color[nxt] == -1 {
                    color[nxt] = 1 - color[node];
                    queue.push_back(nxt);
                } else if color[nxt] == color[node] {
                    return false;
                }
            }
        }
    }
    true
}

fn main() {
    println!("{:?}", is_bipartite(4, vec![vec![0, 1], vec![1, 2], vec![2, 3], vec![3, 0]]));
}
