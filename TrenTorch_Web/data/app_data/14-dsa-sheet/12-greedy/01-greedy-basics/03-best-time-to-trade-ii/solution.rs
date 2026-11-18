// O(n) time, O(1) space
fn max_profit_many(prices: Vec<i64>) -> i64 {
    let mut total = 0;
    for i in 1..prices.len() {
        let diff = prices[i] - prices[i - 1];
        if diff > 0 {
            total += diff;
        }
    }
    total
}

fn main() {
    println!("{:?}", max_profit_many(vec![7, 1, 5, 3, 6, 4]));
}
