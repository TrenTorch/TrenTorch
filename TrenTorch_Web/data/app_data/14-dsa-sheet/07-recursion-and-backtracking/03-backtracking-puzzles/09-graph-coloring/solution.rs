// O(colors^n) time in the worst case (backtracking), O(n + m) space for the graph
fn can_color_graph(n: i64, edges: Vec<Vec<i64>>, colors: i64) -> bool {
    let n = n as usize;
    let mut adj: Vec<Vec<usize>> = vec![Vec::new(); n];
    for edge in &edges {
        let u = edge[0] as usize;
        let v = edge[1] as usize;
        if u == v {
            return false;
        }
        adj[u].push(v);
        adj[v].push(u);
    }
    let mut color: Vec<i64> = vec![-1; n];
    color_go(0, n, colors, &adj, &mut color)
}

fn color_go(i: usize, n: usize, colors: i64, adj: &[Vec<usize>], color: &mut Vec<i64>) -> bool {
    if i == n {
        return true;
    }
    for c in 0..colors {
        if adj[i].iter().all(|&j| color[j] != c) {
            color[i] = c;
            if color_go(i + 1, n, colors, adj, color) {
                return true;
            }
            color[i] = -1;
        }
    }
    false
}

fn main() {
    println!("{:?}", can_color_graph(3, vec![vec![0, 1], vec![1, 2], vec![0, 2]], 3));
}
