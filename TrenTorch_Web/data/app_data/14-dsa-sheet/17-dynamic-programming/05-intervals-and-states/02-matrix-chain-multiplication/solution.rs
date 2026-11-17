// O(n^3) time, O(n^2) space
fn matrix_chain_cost(dims: Vec<i64>) -> i64 {
    let n = dims.len();
    if n < 3 {
        return 0;
    }
    let mut dp = vec![vec![0; n]; n];
    for length in 2..n {
        for i in 0..n - length {
            let j = i + length;
            let mut best = i64::MAX;
            for k in (i + 1)..j {
                let value = dp[i][k] + dp[k][j] + dims[i] * dims[k] * dims[j];
                if value < best {
                    best = value;
                }
            }
            dp[i][j] = best;
        }
    }
    dp[0][n - 1]
}

fn main() {
    println!("{:?}", matrix_chain_cost(vec![10, 30, 5, 60]));
}
