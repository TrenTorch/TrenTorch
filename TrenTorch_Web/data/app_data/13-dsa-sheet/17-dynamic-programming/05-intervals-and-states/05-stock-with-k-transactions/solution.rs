// O(n * min(k, n)) time, O(k) space
fn max_profit_k(k: i64, prices: Vec<i64>) -> i64 {
    if k == 0 || prices.len() < 2 {
        return 0;
    }
    let n = prices.len();
    let k_usize = k as usize;
    if k_usize >= n / 2 {
        let mut profit = 0;
        for i in 1..n {
            let diff = prices[i] - prices[i - 1];
            if diff > 0 {
                profit += diff;
            }
        }
        return profit;
    }
    let mut hold = vec![i64::MIN; k_usize + 1];
    let mut free = vec![0; k_usize + 1];
    for &p in &prices {
        for t in 1..=k_usize {
            hold[t] = hold[t].max(free[t - 1] - p);
            free[t] = free[t].max(hold[t] + p);
        }
    }
    free[k_usize]
}

fn main() {
    println!("{:?}", max_profit_k(2, vec![3, 2, 6, 5, 0, 3]));
}
