// O(n + e) time, O(n + e) space (iterative DFS with discovery and low-link values)
fn articulation_points(n: i64, edges: Vec<Vec<i64>>) -> Vec<i64> {
    let n = n as usize;
    let mut adj: Vec<Vec<usize>> = vec![Vec::new(); n];
    for e in &edges {
        let (a, b) = (e[0] as usize, e[1] as usize);
        adj[a].push(b);
        adj[b].push(a);
    }
    let mut disc: Vec<i64> = vec![-1; n];
    let mut low: Vec<i64> = vec![0; n];
    let mut is_cut = vec![false; n];
    let mut timer: i64 = 0;
    for root in 0..n {
        if disc[root] != -1 {
            continue;
        }
        disc[root] = timer;
        low[root] = timer;
        timer += 1;
        let mut root_children = 0usize;
        // entries are (node, parent, next neighbour index); parent -1 means no parent
        let mut stack: Vec<(usize, i64, usize)> = vec![(root, -1, 0)];
        while let Some((node, parent, i)) = stack.pop() {
            if i < adj[node].len() {
                stack.push((node, parent, i + 1));
                let nxt = adj[node][i];
                if nxt as i64 == parent {
                    continue;
                }
                if disc[nxt] == -1 {
                    disc[nxt] = timer;
                    low[nxt] = timer;
                    timer += 1;
                    if node == root {
                        root_children += 1;
                    }
                    stack.push((nxt, node as i64, 0));
                } else {
                    low[node] = low[node].min(disc[nxt]);
                }
            } else if parent != -1 {
                let p = parent as usize;
                low[p] = low[p].min(low[node]);
                if p != root && low[node] >= disc[p] {
                    is_cut[p] = true;
                }
            }
        }
        if root_children >= 2 {
            is_cut[root] = true;
        }
    }
    (0..n).filter(|&v| is_cut[v]).map(|v| v as i64).collect()
}

fn main() {
    println!("{:?}", articulation_points(5, vec![vec![0, 1], vec![1, 2], vec![2, 0], vec![1, 3], vec![3, 4]]));
}
