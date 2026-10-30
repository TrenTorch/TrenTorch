// O(n) time, O(1) space
fn stock_best_profit(prices: Vec<i64>) -> i64 {
    let mut best: i64 = 0;
    let mut lowest: Option<i64> = None;
    for price in prices {
        match lowest {
            Some(low) => {
                best = best.max(price - low);
                lowest = Some(low.min(price));
            }
            None => {
                lowest = Some(price);
            }
        }
    }
    best
}

fn main() {
    println!("{:?}", stock_best_profit(vec![7, 1, 5, 3, 6, 4]));
}
