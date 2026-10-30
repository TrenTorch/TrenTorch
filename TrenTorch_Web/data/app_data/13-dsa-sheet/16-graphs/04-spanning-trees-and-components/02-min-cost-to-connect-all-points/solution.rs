// O(n^2) time, O(n) space
fn min_cost_connect_points(points: Vec<Vec<i64>>) -> i64 {
    let n = points.len();
    if n == 0 {
        return 0;
    }
    let inf = i64::MAX;
    let mut best = vec![inf; n];
    best[0] = 0;
    let mut used = vec![false; n];
    let mut total = 0i64;

    for _ in 0..n {
        let mut u = None;
        for v in 0..n {
            if !used[v] && (u.is_none() || best[v] < best[u.unwrap()]) {
                u = Some(v);
            }
        }
        let u = u.unwrap();
        used[u] = true;
        total += best[u];
        let ux = points[u][0];
        let uy = points[u][1];
        for v in 0..n {
            if !used[v] {
                let dist = (points[v][0] - ux).abs() + (points[v][1] - uy).abs();
                if dist < best[v] {
                    best[v] = dist;
                }
            }
        }
    }
    total
}

fn main() {
    println!("{:?}", min_cost_connect_points(vec![vec![0, 0], vec![2, 2], vec![3, 10], vec![5, 2], vec![7, 0]]));
}
