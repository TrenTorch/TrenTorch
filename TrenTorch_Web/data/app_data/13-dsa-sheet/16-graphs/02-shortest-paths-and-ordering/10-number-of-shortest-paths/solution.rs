// O((V + E) log V) time, O(V + E) space
fn count_shortest_paths(n: i64, roads: Vec<Vec<i64>>) -> i64 {
    const MOD: i64 = 1_000_000_007;
    let n = n as usize;
    let mut adj = vec![Vec::new(); n];
    for road in roads {
        let a = road[0] as usize;
        let b = road[1] as usize;
        let t = road[2];
        adj[a].push((b, t));
        adj[b].push((a, t));
    }

    let mut dist = vec![i64::MAX; n];
    let mut ways = vec![0; n];
    dist[0] = 0;
    ways[0] = 1;

    use std::collections::BinaryHeap;
    use std::cmp::Reverse;
    let mut heap = BinaryHeap::new();
    heap.push(Reverse((0, 0)));

    while let Some(Reverse((d, u))) = heap.pop() {
        if d > dist[u] {
            continue;
        }
        for &(v, t) in &adj[u] {
            let nd = d + t;
            if nd < dist[v] {
                dist[v] = nd;
                ways[v] = ways[u];
                heap.push(Reverse((nd, v)));
            } else if nd == dist[v] {
                ways[v] = (ways[v] + ways[u]) % MOD;
            }
        }
    }

    ways[n - 1] % MOD
}

fn main() {
    println!("{:?}", count_shortest_paths(4, vec![vec![0, 1, 1], vec![0, 2, 1], vec![1, 3, 1], vec![2, 3, 1]]));
}
