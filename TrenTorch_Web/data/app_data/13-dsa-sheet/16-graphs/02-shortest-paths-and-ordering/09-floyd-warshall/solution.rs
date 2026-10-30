// O(n^3) time, O(n^2) space
fn all_pairs_shortest(n: i64, edges: Vec<Vec<i64>>) -> Vec<Vec<i64>> {
    let n_usize = n as usize;
    const INF: i64 = 1_000_000_000_000_000; // 1e15
    let mut dist = vec![vec![INF; n_usize]; n_usize];
    for i in 0..n_usize {
        dist[i][i] = 0;
    }
    for edge in edges {
        let a = edge[0] as usize;
        let b = edge[1] as usize;
        let w = edge[2];
        if w < dist[a][b] {
            dist[a][b] = w;
        }
    }
    for k in 0..n_usize {
        for i in 0..n_usize {
            let dik = dist[i][k];
            if dik == INF {
                continue;
            }
            for j in 0..n_usize {
                let new_dist = dik + dist[k][j];
                if new_dist < dist[i][j] {
                    dist[i][j] = new_dist;
                }
            }
        }
    }
    for i in 0..n_usize {
        for j in 0..n_usize {
            if dist[i][j] == INF {
                dist[i][j] = -1;
            }
        }
    }
    dist
}

fn main() {
    println!("{:?}", all_pairs_shortest(3, vec![vec![0, 1, 4], vec![1, 2, 1], vec![0, 2, 7]]));
}
