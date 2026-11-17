// O(n + e) time, O(n + e) space
fn count_components(n: i64, edges: Vec<Vec<i64>>) -> i64 {
    let n = n as usize;
    let mut adj: Vec<Vec<usize>> = vec![Vec::new(); n];
    for e in &edges {
        let a = e[0] as usize;
        let b = e[1] as usize;
        adj[a].push(b);
        adj[b].push(a);
    }
    let mut seen = vec![false; n];
    let mut count: i64 = 0;
    for start in 0..n {
        if seen[start] {
            continue;
        }
        count += 1;
        seen[start] = true;
        let mut stack = vec![start];
        while let Some(node) = stack.pop() {
            for &nxt in &adj[node] {
                if !seen[nxt] {
                    seen[nxt] = true;
                    stack.push(nxt);
                }
            }
        }
    }
    count
}

fn main() {
    println!("{:?}", count_components(5, vec![vec![0, 1], vec![1, 2], vec![3, 4]]));
}
