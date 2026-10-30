fn tsp(dist: Vec<Vec<i64>>) -> i64 {
    // O(n^2 * 2^n) time, O(n * 2^n) space
    let n = dist.len();
    if n <= 1 {
        return 0;
    }
    let full = (1 << n) - 1;
    const INF: i64 = i64::MAX / 4;
    let mut best = vec![vec![INF; n]; 1 << n];
    best[1][0] = 0;
    for mask in 1..=full {
        if (mask & 1) == 0 {
            continue;
        }
        for last in 0..n {
            let cost = best[mask][last];
            if cost == INF {
                continue;
            }
            for nxt in 0..n {
                if (mask >> nxt) & 1 == 0 {
                    let new_mask = mask | (1 << nxt);
                    let new_cost = cost + dist[last][nxt];
                    if new_cost < best[new_mask][nxt] {
                        best[new_mask][nxt] = new_cost;
                    }
                }
            }
        }
    }
    let mut ans = INF;
    for last in 1..n {
        let cost = best[full][last];
        if cost != INF {
            let total = cost + dist[last][0];
            if total < ans {
                ans = total;
            }
        }
    }
    ans
}

fn main() {
    println!("{:?}", tsp(vec![vec![0, 10, 15, 20], vec![10, 0, 35, 25], vec![15, 35, 0, 30], vec![20, 25, 30, 0]]));
}
