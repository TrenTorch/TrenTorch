use std::cmp::Reverse;
use std::collections::BinaryHeap;

// O((n + e) log n) time, O(n + e) space
fn shortest_distances(n: i64, edges: Vec<Vec<i64>>, source: i64) -> Vec<i64> {
    let n = n as usize;
    let mut adj: Vec<Vec<(usize, i64)>> = vec![Vec::new(); n];
    for e in &edges {
        adj[e[0] as usize].push((e[1] as usize, e[2]));
    }
    const INF: i64 = i64::MAX;
    let src = source as usize;
    let mut dist = vec![INF; n];
    dist[src] = 0;
    let mut heap = BinaryHeap::new();
    heap.push(Reverse((0i64, src)));
    while let Some(Reverse((d, u))) = heap.pop() {
        if d > dist[u] {
            continue;
        }
        for &(v, w) in &adj[u] {
            if d + w < dist[v] {
                dist[v] = d + w;
                heap.push(Reverse((dist[v], v)));
            }
        }
    }
    dist.into_iter()
        .map(|d| if d < INF { d } else { -1 })
        .collect()
}

fn main() {
    println!("{:?}", shortest_distances(3, vec![vec![0, 1, 4], vec![0, 2, 1], vec![2, 1, 2]], 0));
}
