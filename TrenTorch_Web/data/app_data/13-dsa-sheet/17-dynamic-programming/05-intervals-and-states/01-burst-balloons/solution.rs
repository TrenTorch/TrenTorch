// O(n^3) time, O(n^2) space
fn max_coins(nums: Vec<i64>) -> i64 {
    let mut a = Vec::with_capacity(nums.len() + 2);
    a.push(1);
    a.extend(nums);
    a.push(1);
    let n = a.len();
    let mut dp = vec![vec![0; n]; n];

    for length in 2..n {
        for i in 0..n - length {
            let j = i + length;
            let mut best = 0;
            for k in i + 1..j {
                let value = dp[i][k] + dp[k][j] + a[i] * a[k] * a[j];
                if value > best {
                    best = value;
                }
            }
            dp[i][j] = best;
        }
    }
    dp[0][n - 1]
}

fn main() {
    println!("{:?}", max_coins(vec![3, 1, 5, 8]));
}
