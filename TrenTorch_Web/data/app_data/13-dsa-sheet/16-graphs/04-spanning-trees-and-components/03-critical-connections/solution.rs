// O(n + e) time, O(n + e) space (iterative Tarjan bridge search)
fn critical_connections(n: i64, connections: Vec<Vec<i64>>) -> Vec<Vec<i64>> {
    let n = n as usize;
    let mut adj: Vec<Vec<usize>> = vec![Vec::new(); n];
    for c in &connections {
        let (a, b) = (c[0] as usize, c[1] as usize);
        adj[a].push(b);
        adj[b].push(a);
    }
    let mut disc: Vec<i64> = vec![-1; n];
    let mut low: Vec<i64> = vec![0; n];
    let mut bridges: Vec<Vec<i64>> = Vec::new();
    let mut timer: i64 = 0;
    for root in 0..n {
        if disc[root] != -1 {
            continue;
        }
        disc[root] = timer;
        low[root] = timer;
        timer += 1;
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
                    stack.push((nxt, node as i64, 0));
                } else {
                    low[node] = low[node].min(disc[nxt]);
                }
            } else if parent != -1 {
                let p = parent as usize;
                low[p] = low[p].min(low[node]);
                if low[node] > disc[p] {
                    let (a, b) = (p.min(node), p.max(node));
                    bridges.push(vec![a as i64, b as i64]);
                }
            }
        }
    }
    bridges.sort();
    bridges
}

fn main() {
    println!("{:?}", critical_connections(4, vec![vec![0, 1], vec![1, 2], vec![2, 0], vec![1, 3]]));
}
