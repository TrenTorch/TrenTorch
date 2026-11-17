// O(n^2) time, O(n^2) space
fn min_cost_cut(length: i64, cuts: Vec<i64>) -> i64 {
    let mut points = vec![0];
    let mut sorted_cuts = cuts;
    sorted_cuts.sort_unstable();
    points.extend(sorted_cuts);
    points.push(length);
    let n = points.len();

    let mut dp = vec![vec![0i64; n]; n];
    let mut best_cut = vec![vec![0usize; n]; n];

    for i in 0..n - 1 {
        best_cut[i][i + 1] = i + 1;
    }

    for span in 2..n {
        for i in 0..(n - span) {
            let j = i + span;
            let low = std::cmp::max(i + 1, best_cut[i][j - 1]);
            let high = std::cmp::min(j - 1, best_cut[i + 1][j]);

            let mut best_val = i64::MAX;
            let mut best_k = low;
            for k in low..=high {
                let val = dp[i][k] + dp[k][j];
                if val < best_val {
                    best_val = val;
                    best_k = k;
                }
            }
            dp[i][j] = best_val + points[j] - points[i];
            best_cut[i][j] = best_k;
        }
    }

    dp[0][n - 1]
}

fn main() {
    println!("{:?}", min_cost_cut(7, vec![1, 3, 4, 5]));
}
