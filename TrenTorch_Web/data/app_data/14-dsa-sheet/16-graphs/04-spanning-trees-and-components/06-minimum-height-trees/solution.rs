// O(n) time, O(n) space (peel leaves layer by layer)
fn min_height_trees(n: i64, edges: Vec<Vec<i64>>) -> Vec<i64> {
    if n <= 2 {
        return (0..n).map(|v| v as i64).collect();
    }
    let n = n as usize;
    let mut adj: Vec<Vec<usize>> = vec![Vec::new(); n];
    for e in &edges {
        let (a, b) = (e[0] as usize, e[1] as usize);
        adj[a].push(b);
        adj[b].push(a);
    }
    let mut degree: Vec<i64> = adj.iter().map(|a| a.len() as i64).collect();
    let mut leaves: Vec<usize> = (0..n).filter(|&v| degree[v] == 1).collect();
    let mut remaining = n;
    while remaining > 2 {
        remaining -= leaves.len();
        let mut next: Vec<usize> = Vec::new();
        for &leaf in &leaves {
            for &other in &adj[leaf] {
                degree[other] -= 1;
                if degree[other] == 1 {
                    next.push(other);
                }
            }
        }
        leaves = next;
    }
    let mut out: Vec<i64> = leaves.into_iter().map(|v| v as i64).collect();
    out.sort();
    out
}

fn main() {
    println!("{:?}", min_height_trees(6, vec![vec![3, 0], vec![3, 1], vec![3, 2], vec![3, 4], vec![5, 4]]));
}
