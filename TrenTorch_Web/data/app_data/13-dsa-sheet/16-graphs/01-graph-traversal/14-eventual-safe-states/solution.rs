// O(n + m) time, O(n + m) space
use std::collections::VecDeque;

fn eventual_safe_nodes(n: i64, edges: Vec<Vec<i64>>) -> Vec<i64> {
    let n = n as usize;
    let mut rev = vec![Vec::new(); n];
    let mut out_degree = vec![0; n];
    for edge in edges {
        let a = edge[0] as usize;
        let b = edge[1] as usize;
        rev[b].push(a);
        out_degree[a] += 1;
    }
    let mut queue = VecDeque::new();
    for v in 0..n {
        if out_degree[v] == 0 {
            queue.push_back(v);
        }
    }
    let mut safe = vec![false; n];
    while let Some(node) = queue.pop_front() {
        safe[node] = true;
        for &p in &rev[node] {
            out_degree[p] -= 1;
            if out_degree[p] == 0 {
                queue.push_back(p);
            }
        }
    }
    let mut result = Vec::new();
    for v in 0..n {
        if safe[v] {
            result.push(v as i64);
        }
    }
    result
}

fn main() {
    println!("{:?}", eventual_safe_nodes(7, vec![vec![0, 1], vec![0, 2], vec![1, 2], vec![1, 3], vec![2, 5], vec![3, 0], vec![4, 5]]));
}
