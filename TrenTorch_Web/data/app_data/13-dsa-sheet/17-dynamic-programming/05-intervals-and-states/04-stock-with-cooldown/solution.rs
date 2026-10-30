// O(n) time, O(1) space
fn max_profit_cooldown(prices: Vec<i64>) -> i64 {
    let mut hold = i64::MIN;
    let mut sold = 0;
    let mut rest = 0;
    for price in prices {
        let new_hold = hold.max(rest - price);
        let new_sold = hold + price;
        let new_rest = rest.max(sold);
        hold = new_hold;
        sold = new_sold;
        rest = new_rest;
    }
    sold.max(rest)
}

fn main() {
    println!("{:?}", max_profit_cooldown(vec![1, 2, 3, 0, 2]));
}
